import sqlite3
import os

DB_PATH = os.environ.get("DB_PATH", "flighthub.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS flights (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            airline         TEXT NOT NULL,
            origin          TEXT NOT NULL,
            destination     TEXT NOT NULL,
            departure_time  TEXT NOT NULL,
            duration_minutes INTEGER NOT NULL,
            price           REAL NOT NULL,
            seats_available INTEGER NOT NULL CHECK(seats_available >= 0)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            reference       TEXT UNIQUE NOT NULL,
            flight_id       INTEGER NOT NULL REFERENCES flights(id),
            passenger_name  TEXT NOT NULL,
            passport_number TEXT NOT NULL,
            seat            TEXT NOT NULL,
            status          TEXT NOT NULL DEFAULT 'confirmed',
            created_at      TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)

    # Seed only if flights table is empty
    count = conn.execute("SELECT COUNT(*) FROM flights").fetchone()[0]
    if count == 0:
        flights = [
            # LHR → JFK
            ("BritAir",  "London",    "New York",    "2026-08-01 08:00", 435, 320.00, 5),
            ("BritAir",  "London",    "New York",    "2026-08-01 14:00", 440, 285.00, 3),
            ("BritAir",  "London",    "New York",    "2026-08-02 09:00", 435, 310.00, 8),
            # JFK → LHR
            ("TransAtl", "New York",  "London",      "2026-08-01 18:00", 420, 298.00, 6),
            ("TransAtl", "New York",  "London",      "2026-08-02 22:00", 415, 275.00, 4),
            # DXB → LHR
            ("GulfWings","Dubai",     "London",      "2026-08-01 02:00", 415, 410.00, 2),
            ("GulfWings","Dubai",     "London",      "2026-08-03 10:00", 420, 390.00, 7),
            # LHR → DXB
            ("GulfWings","London",    "Dubai",       "2026-08-01 22:00", 410, 395.00, 5),
            # KHI → DXB
            ("PakAir",   "Karachi",   "Dubai",       "2026-08-01 06:00", 150,  95.00, 5),
            ("PakAir",   "Karachi",   "Dubai",       "2026-08-01 13:00", 150,  85.00, 0),  # full flight for test
            ("PakAir",   "Karachi",   "Dubai",       "2026-08-01 20:00", 155,  90.00, 3),
            # LHR → SIN
            ("SkyLink",  "London",    "Singapore",   "2026-08-05 23:00", 780, 620.00, 10),
            # SIN → LHR
            ("SkyLink",  "Singapore", "London",      "2026-08-10 01:00", 800, 610.00, 6),
            # NYC → LAX
            ("CoastAir", "New York",  "Los Angeles", "2026-08-01 07:30", 330, 180.00, 5),
            ("CoastAir", "New York",  "Los Angeles", "2026-08-01 15:00", 325, 165.00, 9),
        ]
        conn.executemany(
            """INSERT INTO flights
               (airline, origin, destination, departure_time, duration_minutes, price, seats_available)
               VALUES (?,?,?,?,?,?,?)""",
            flights,
        )

    conn.commit()
    conn.close()
