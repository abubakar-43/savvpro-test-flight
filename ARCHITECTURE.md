# FlightHub — Architecture

## Data Model

### `flights`

| Column             | Type    | Description                   |
|--------------------|---------|-------------------------------|
| id                 | INTEGER | Primary key, auto-increment   |
| airline            | TEXT    | Airline name                  |
| origin             | TEXT    | Departure city                |
| destination        | TEXT    | Arrival city                  |
| departure_time     | TEXT    | ISO datetime string           |
| duration_minutes   | INTEGER | Flight duration               |
| price              | REAL    | Price per seat (USD)          |
| seats_available    | INTEGER | Remaining bookable seats ≥ 0  |

### `bookings`

| Column          | Type    | Description                        |
|-----------------|---------|------------------------------------|
| id              | INTEGER | Primary key, auto-increment        |
| reference       | TEXT    | Unique booking ref, format FH-XXXX |
| flight_id       | INTEGER | Flight ID                          |
| passenger_name  | TEXT    | Full name of the passenger         |
| passport_number | TEXT    | Passport ID                        |
| seat            | TEXT    | Free-text seat number              |
| status          | TEXT    | `confirmed` or `cancelled`         |
| created_at      | TEXT    | UTC datetime of booking creation   |

---

## API Design

| Method | Path                  | Description                         | Status codes       |
|--------|-----------------------|-------------------------------------|--------------------|
| GET    | /flights              | List/search flights                 | 200                |
| GET    | /flights/{id}         | Get single flight                   | 200, 404           |
| POST   | /bookings             | Create a booking                    | 201, 409, 422, 404 |
| GET    | /bookings             | Search bookings by name/reference   | 200, 400           |
| DELETE | /bookings/{reference} | Cancel a booking                    | 200, 404, 409      |

All responses are JSON. Pydantic models handle input validation; invalid payloads automatically return `422 Unprocessable Entity` with field-level error details.

---

## Ambiguity Resolutions

### 1. "Handle overbooking appropriately"

**Decision:** When a booking is attempted on a flight with 0 available seats, the API returns HTTP `409 Conflict` with:

```json
{
  "error": "No seats available on this flight",
  "alternatives": [ ...up to 3 flights on same route with seats... ]
}
```

Alternatives are the flights on the **same origin→destination route** ordered by proximity to the full flight's departure time (`ABS(departure_epoch - full_flight_epoch)`). This gives staff the most useful options — flights closest in time to what the passenger originally wanted.

### 2. "Display relevant flight information"

The UI prioritises the information a travel agent needs at a glance when presenting a flight to a customer:

1. **Route** (origin → destination) in large type — the most important identifier.
2. **Airline, date, time, duration** — secondary context.
3. **Price per seat** — prominently displayed so agents can quote instantly.
4. **Seat availability** — colour-coded badge (green/amber/red) so overbooking risk is immediately visible.

The layout is a card list (not a table) so each flight is scannable independently and the Book button is immediately reachable without horizontal scrolling.