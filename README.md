# FlightHub ✈️

A minimal internal flight search and booking tool for travel agency staff.

## Stack

| Layer    | Technology                 |
|----------|----------------------------|
| Backend  | Python 3.11.6 · FastAPI · SQLite |
| Frontend | Node.js v20.20.2 · Express · Vanilla JS |

---

## Prerequisites

- Python 3.11.6
- Node.js v20.20.2
- pip

---

## Setup & Run

### 1 — Backend

```bash
cd backend (important step to avoid module import path errors)
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.  
Interactive docs (Swagger UI) at `http://localhost:8000/docs`.

The SQLite database file (`flighthub.db`) is created automatically on first run, with seed flight data included.

### 2 — Frontend

In a **separate terminal**:

```bash
cd frontend
npm install
npm start
```

The UI will be available at `http://localhost:3000`.

> **Important:** The frontend calls the backend at `http://localhost:8000`. Make sure the backend is running first.

---

## Running Tests

From the `backend/` directory:

```bash
set PYTHONPATH=C:\Users\haier\Desktop\savvpro-test-flight\backend
pytest ../tests/test_flighthub.py -v
```

All 5 tests should pass. Tests use a temporary SQLite file (isolated from production data).