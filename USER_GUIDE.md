# FlightHub — User Guide


Open `http://localhost:3000` in a browser after starting both servers.

The app has three sections accessible from the top navigation:

### Flights (default view)

Displays all available flights. Use the search bar to filter by:
- **From** — origin city (e.g. `London`)
- **To** — destination city (e.g. `New York`)
- **Date** — departure date

Each flight card shows the airline, route, departure time, duration, price, and a colour-coded seat availability badge:
- 🟢 Green — plenty of seats
- 🟠 Amber — 1–2 seats left
- 🔴 Red — full

Click **Book** to open the booking modal. Fill in passenger name, passport number, and seat (e.g. `12A`), then click **Confirm Booking**.

### My Bookings

Search by passenger name or booking reference to retrieve existing bookings.

### Cancel

Enter a booking reference (format `FH-XXXXXXXX`) to cancel a reservation. The seat is immediately returned to the flight.

---


### List all flights

```bash
curl http://localhost:8000/flights
```

### Search flights by route and date

```bash
curl "http://localhost:8000/flights?origin=London&destination=New%20York&departure_date=2025-08-01"
```

### Book a flight

```bash
curl -X POST http://localhost:8000/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "flight_id": 1,
    "passenger_name": "Jane Doe",
    "passport_number": "A12345678",
    "seat": "14C"
  }'
```

**Success response (201):**
```json
{
  "reference": "FH-3A7F9B2C",
  "status": "confirmed",
  "message": "Booking confirmed"
}
```

### View bookings by name

```bash
curl "http://localhost:8000/bookings?name=Jane"
```

### View booking by reference

```bash
curl "http://localhost:8000/bookings?reference=FH-3A7F9B2C"
```

### Cancel a booking

```bash
curl -X DELETE http://localhost:8000/bookings/FH-3A7F9B2C
```

**Response:**
```json
{
  "message": "Booking FH-3A7F9B2C has been cancelled"
}
```