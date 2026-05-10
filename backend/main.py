from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date
import uuid
from contextlib import asynccontextmanager

from database import init_db, get_db_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()   # startup code
    yield


app = FastAPI(
    title="FlightHub API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


# ── Models ────────────────────────────────────────────────────────────────────

class BookingRequest(BaseModel):
    flight_id: int
    passenger_name: str
    passport_number: str
    seat: str

    @field_validator("passenger_name")
    @classmethod
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("passenger_name must not be empty")
        return v.strip()

    @field_validator("passport_number")
    @classmethod
    def passport_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("passport_number must not be empty")
        return v.strip()

    @field_validator("seat")
    @classmethod
    def seat_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("seat must not be empty")
        return v.strip()


# ── Flights ───────────────────────────────────────────────────────────────────

@app.get("/flights")
def list_flights(
    origin: Optional[str] = Query(None),
    destination: Optional[str] = Query(None),
    departure_date: Optional[date] = Query(None),
):
    conn = get_db_connection()
    query = "SELECT * FROM flights WHERE 1=1"
    params = []

    if origin:
        query += " AND LOWER(origin) = LOWER(?)"
        params.append(origin)
    if destination:
        query += " AND LOWER(destination) = LOWER(?)"
        params.append(destination)
    if departure_date:
        query += " AND DATE(departure_time) = ?"
        params.append(str(departure_date))

    flights = conn.execute(query, params).fetchall()
    conn.close()

    if not flights and (origin or destination or departure_date):
        return {"flights": [], "message": "No flights found matching your search criteria."}

    return {"flights": [dict(f) for f in flights]}


@app.get("/flights/{flight_id}")
def get_flight(flight_id: int):
    conn = get_db_connection()
    flight = conn.execute("SELECT * FROM flights WHERE id = ?", (flight_id,)).fetchone()
    conn.close()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    return dict(flight)


# ── Bookings ──────────────────────────────────────────────────────────────────

@app.post("/bookings")
def create_booking(req: BookingRequest, response: Response):
    conn = get_db_connection()

    flight = conn.execute(
        "SELECT * FROM flights WHERE id = ?", (req.flight_id,)
    ).fetchone()

    if not flight:
        conn.close()
        raise HTTPException(status_code=404, detail="Flight not found")

    if flight["seats_available"] <= 0:
        alternatives = conn.execute(
            """
            SELECT * FROM flights
            WHERE LOWER(origin) = LOWER(?) AND LOWER(destination) = LOWER(?)
              AND id != ? AND seats_available > 0
            ORDER BY ABS(strftime('%s', departure_time) - strftime('%s', ?))
            LIMIT 3
            """,
            (flight["origin"], flight["destination"], flight["id"], flight["departure_time"]),
        ).fetchall()
        conn.close()
        # 409 Conflict — no seats, include alternatives
        response.status_code = 409
        return {
            "error": "No seats available on this flight",
            "alternatives": [dict(a) for a in alternatives],
        }

    # Check seat not already taken
    taken = conn.execute(
        "SELECT id FROM bookings WHERE flight_id = ? AND seat = ? AND status = 'confirmed'",
        (req.flight_id, req.seat),
    ).fetchone()
    if taken:
        conn.close()
        raise HTTPException(
            status_code=409, detail=f"Seat {req.seat} is already taken on this flight"
        )

    reference = "FH-" + uuid.uuid4().hex[:8].upper()

    conn.execute(
        """
        INSERT INTO bookings (reference, flight_id, passenger_name, passport_number, seat, status)
        VALUES (?, ?, ?, ?, ?, 'confirmed')
        """,
        (reference, req.flight_id, req.passenger_name, req.passport_number, req.seat),
    )
    conn.execute(
        "UPDATE flights SET seats_available = seats_available - 1 WHERE id = ?",
        (req.flight_id,),
    )
    conn.commit()
    conn.close()

    response.status_code = 201
    return {"reference": reference, "status": "confirmed", "message": "Booking confirmed"}


@app.get("/bookings")
def search_bookings(
    name: Optional[str] = Query(None),
    reference: Optional[str] = Query(None),
):
    if not name and not reference:
        raise HTTPException(
            status_code=400, detail="Provide at least one of: name, reference"
        )

    conn = get_db_connection()
    query = """
        SELECT b.*, f.origin, f.destination, f.departure_time, f.duration_minutes,
               f.price, f.airline
        FROM bookings b
        JOIN flights f ON b.flight_id = f.id
        WHERE 1=1
    """
    params = []

    if name:
        query += " AND LOWER(b.passenger_name) LIKE LOWER(?)"
        params.append(f"%{name}%")
    if reference:
        query += " AND UPPER(b.reference) = UPPER(?)"
        params.append(reference)

    rows = conn.execute(query, params).fetchall()
    conn.close()

    if not rows:
        return {"bookings": [], "message": "No bookings found"}

    return {"bookings": [dict(r) for r in rows]}


@app.delete("/bookings/{reference}")
def cancel_booking(reference: str):
    conn = get_db_connection()

    booking = conn.execute(
        "SELECT * FROM bookings WHERE UPPER(reference) = UPPER(?)", (reference,)
    ).fetchone()

    if not booking:
        conn.close()
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking["status"] == "cancelled":
        conn.close()
        raise HTTPException(status_code=409, detail="Booking is already cancelled")

    conn.execute(
        "UPDATE bookings SET status = 'cancelled' WHERE UPPER(reference) = UPPER(?)",
        (reference,),
    )
    conn.execute(
        "UPDATE flights SET seats_available = seats_available + 1 WHERE id = ?",
        (booking["flight_id"],),
    )
    conn.commit()
    conn.close()

    return {"message": f"Booking {reference} has been cancelled"}
