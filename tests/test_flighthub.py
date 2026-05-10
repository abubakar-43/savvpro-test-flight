"""
FlightHub — 5 required tests
Run from /backend directory:
    pytest ../tests/test_flighthub.py -v
"""
import os, tempfile, pytest

# Use a temp file so all connections share the same DB
_db_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_db_file.close()
os.environ["DB_PATH"] = _db_file.name

from fastapi.testclient import TestClient
from main import app
from database import init_db, get_db_connection

init_db()
client = TestClient(app)


# ── Helpers ──────────────────────────────────────────────────────────────────

def reset_db():
    conn = get_db_connection()
    conn.execute("DELETE FROM bookings")
    conn.execute("DELETE FROM flights")
    try:
        conn.execute("DELETE FROM sqlite_sequence WHERE name IN ('bookings','flights')")
    except Exception:
        pass
    conn.commit()
    conn.close()


def add_flight(seats: int, departure_time: str = "2025-08-01 08:00",
               origin: str = "TestCity", destination: str = "DestCity") -> int:
    conn = get_db_connection()
    cur = conn.execute(
        """INSERT INTO flights
           (airline, origin, destination, departure_time, duration_minutes, price, seats_available)
           VALUES ('TestAir',?,?,?,120,100.0,?)""",
        (origin, destination, departure_time, seats),
    )
    conn.commit()
    fid = cur.lastrowid
    conn.close()
    return fid


def make_booking(flight_id: int, seat: str = "1A"):
    return client.post("/bookings", json={
        "flight_id": flight_id,
        "passenger_name": "Test Passenger",
        "passport_number": "AB123456",
        "seat": seat,
    })


# ════════════════════════════════════════════════════════════════════════════
# Test 1 — Booking a seat reduces available seats
# ════════════════════════════════════════════════════════════════════════════

def test_booking_reduces_seats():
    """Flight starts with 5 seats; after booking, seats_available becomes 4."""
    reset_db()
    fid = add_flight(seats=5)

    res = make_booking(fid)
    assert res.status_code == 201, res.json()

    flight = client.get(f"/flights/{fid}").json()
    assert flight["seats_available"] == 4


# ════════════════════════════════════════════════════════════════════════════
# Test 2 — Cannot overbook a full flight; alternatives returned
# ════════════════════════════════════════════════════════════════════════════

def test_cannot_overbook_returns_alternatives():
    """Flight has 0 seats — returns error and closest available alternatives."""
    reset_db()
    full_id = add_flight(seats=0, departure_time="2025-08-01 10:00")
    add_flight(seats=3, departure_time="2025-08-01 12:00")
    add_flight(seats=2, departure_time="2025-08-01 08:00")

    res = make_booking(full_id)
    body = res.json()

    assert res.status_code == 409
    assert "error" in body
    assert "No seats available" in body["error"]
    assert "alternatives" in body
    assert len(body["alternatives"]) > 0
    for alt in body["alternatives"]:
        assert alt["seats_available"] > 0


# ════════════════════════════════════════════════════════════════════════════
# Test 3 — Cancelling a booking restores seat availability
# ════════════════════════════════════════════════════════════════════════════

def test_cancel_restores_seat_availability():
    """5 seats → book → 4 seats → cancel → 5 seats."""
    reset_db()
    fid = add_flight(seats=5)

    book_res = make_booking(fid)
    assert book_res.status_code == 201
    ref = book_res.json()["reference"]

    assert client.get(f"/flights/{fid}").json()["seats_available"] == 4

    cancel_res = client.delete(f"/bookings/{ref}")
    assert cancel_res.status_code == 200

    assert client.get(f"/flights/{fid}").json()["seats_available"] == 5


# ════════════════════════════════════════════════════════════════════════════
# Test 4 — Search by origin / destination / date returns correct results
# ════════════════════════════════════════════════════════════════════════════

def test_search_flights_filters_correctly():
    """Matching flights returned; non-matching excluded."""
    reset_db()

    conn = get_db_connection()
    conn.execute("""INSERT INTO flights
        (airline,origin,destination,departure_time,duration_minutes,price,seats_available)
        VALUES ('Air1','Paris','Berlin','2025-09-10 07:00',90,150.0,5)""")
    conn.execute("""INSERT INTO flights
        (airline,origin,destination,departure_time,duration_minutes,price,seats_available)
        VALUES ('Air2','Paris','Berlin','2025-09-10 15:00',95,170.0,3)""")
    conn.execute("""INSERT INTO flights
        (airline,origin,destination,departure_time,duration_minutes,price,seats_available)
        VALUES ('Air3','Rome','Madrid','2025-09-11 09:00',120,200.0,8)""")
    conn.commit()
    conn.close()

    res = client.get("/flights", params={
        "origin": "Paris",
        "destination": "Berlin",
        "departure_date": "2025-09-10",
    })
    assert res.status_code == 200
    flights = res.json()["flights"]

    assert len(flights) == 2
    for f in flights:
        assert f["origin"].lower() == "paris"
        assert f["destination"].lower() == "berlin"
    assert "Air3" not in [f["airline"] for f in flights]


# ════════════════════════════════════════════════════════════════════════════
# Test 5 — Invalid booking returns HTTP 422
# ════════════════════════════════════════════════════════════════════════════

def test_invalid_booking_returns_422():
    """Missing/empty required fields → 422 Unprocessable Entity."""
    reset_db()
    fid = add_flight(seats=5)

    # Missing passport_number
    r1 = client.post("/bookings", json={
        "flight_id": fid, "passenger_name": "Test Passenger", "seat": "3B",
    })
    assert r1.status_code == 422, f"Expected 422, got {r1.status_code}"

    # Missing passenger_name
    r2 = client.post("/bookings", json={
        "flight_id": fid, "passport_number": "XX999", "seat": "4C",
    })
    assert r2.status_code == 422, f"Expected 422, got {r2.status_code}"

    # Empty strings (custom validator → 422)
    r3 = client.post("/bookings", json={
        "flight_id": fid, "passenger_name": "", "passport_number": "", "seat": "5D",
    })
    assert r3.status_code == 422, f"Expected 422, got {r3.status_code}"
