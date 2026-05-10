# ✈️ Assessment Test 1 — FlightHub: Flight Search & Booking System

## Overview

You are tasked with building **FlightHub** — a simple full-stack flight search and booking application. This assessment evaluates your ability to understand requirements, plan a solution, develop it using an **AI coding agent**, and deliver a working product.

**Time Limit:** 4 Hours
**AI Tool:** Any AI coding agent of your choice (Claude Code, GitHub Copilot, Cursor, Codex, Qwen Coder, Gemini Code Assist, or any other paid or free tool)
**Stack:** Python (FastAPI) for backend · Node.js (Express) for frontend
**Deliverable:** A working GitHub repository pushed before the deadline

---

## The Scenario

FlightHub is a minimal internal tool for a small travel agency. Staff need to search available flights, book seats for passengers, view current bookings, and cancel them if needed. There is no payment system — bookings are confirmed immediately.

---

## Functional Requirements

### 1. Flight Listings
- Display a list of all available flights
- Each flight must show: origin, destination, departure date and time, duration, price per seat, and number of seats available

### 2. Flight Search
- Allow filtering flights by origin, destination, and departure date
- Return matching results or an appropriate message if none found

### 3. Book a Flight
- A user can book a seat on an available flight
- Required fields: passenger full name, passport number, seat selection
- A booking must generate a unique booking reference
- **Handle overbooking appropriately** *(your decision — document it)*

### 4. View Bookings
- Retrieve all bookings by passenger name or booking reference
- Each booking must show: reference, flight details, passenger name, seat, booking status

### 5. Cancel a Booking
- A passenger can cancel using their booking reference
- Cancellation must update seat availability on the flight

---

## Non-Functional Requirements

- All API endpoints must return appropriate HTTP status codes
- Invalid inputs must return clear validation error messages
- The frontend must connect to and consume the backend API
- SQLite is sufficient — no external database required
- The app must be runnable locally following your README

---

## Deliberate Ambiguities

The following are intentionally left open. Make a decision and document your reasoning in `ARCHITECTURE.md`:

1. **"Handle overbooking appropriately"** — What is your rule when the last seat is taken?
2. **"Display relevant flight information"** — You decide what the UI prioritises and how it is laid out

---

## What You Must Deliver

| File / Folder | Description |
|---|---|
| `README.md` | Setup instructions, how to run backend and frontend, assumptions |
| `ARCHITECTURE.md` | Data model, API design, how you resolved ambiguities |
| `AI_USAGE.md` | Which AI tool you used, key prompts, what it got wrong, how you corrected it |
| `USER_GUIDE.md` | How to use the app — curl examples or UI screenshots |
| `/backend/` | FastAPI application, runnable with `uvicorn` |
| `/frontend/` | Express application serving an HTML UI |
| `/tests/` | Minimum 3 tests — at least one must test a business rule |
| `.gitignore` | Appropriate entries |

---
5
## Git Requirements

- Initialise the repo from scratch — no starter templates
- At least **5 meaningful commits** — not one final dump
- Clear commit messages (e.g. `feat: add booking cancellation endpoint`)
- Push to a public GitHub repository and share the link

---

## Constraints

- You **must** use at least one AI coding agent actively — it is a core part of the assessment
- No pre-built boilerplate or starter templates
- No paid APIs or external services — everything runs locally
- Standard open-source libraries are permitted (FastAPI, SQLAlchemy, Express, etc.)
- Internet access for documentation only

---

## Evaluation Criteria Summary

| Area | Weight |
|---|---|
| Requirements coverage | 10% |
| Architecture & planning | 10% |
| Backend implementation | 25% |
| Frontend implementation | 15% |
| AI coding agent usage quality | 20% |
| Testing | 10% |
| Git discipline | 5% |
| Documentation | 5% |

---

## Time Guidance (Suggested)

| Phase | Time |
|---|---|
| Read brief, plan, draft ARCHITECTURE.md | 30 min |
| Backend development + tests | 90 min |
| Frontend development | 60 min |
| Integration, bug fixing, final tests | 30 min |
| Documentation, git cleanup, push | 30 min |

---

*Good luck. The quality of your thinking matters more than the quantity of your code.*
