# AI Usage

## Tool Used

**Claude Sonnet 4.6** and **ChatGPT**


1. **Initial scaffold**  
The AI was given the full specification with 5 defined tests and it produced all code, tests, and documentation files iteratively, fixing issues as they arose.


2. Partial Search Matching for Flights
Enhanced the flight search functionality so that users no longer need to enter the complete city name in the `FROM` field.
The search now supports partial and substring matching.
### Example
- Input: `York`
- Result: Flights from `New York` are displayed.


3. Booking Confirmation Page
Implemented a booking confirmation page that appears immediately after a successful seat booking.
### Features
- Displays a booking success message.
- Shows the reference number of the booked seat/ticket.
- Improves user feedback and booking transparency.


4. Instant Seat Availability Updates After Cancellation
Fixed the issue where cancelled tickets were not immediately reflected on the flights page unless the page was manually reloaded.
### Improvement
- Flight seat availability now updates instantly after a ticket cancellation.
- Eliminated the need for manual page refreshes.
- Improved synchronization between booking and flight listing views.


5. Input Validation Enhancements
### Name Field Validation
Added validation to ensure that the passenger name field only accepts:
- Alphabets (`A-Z`, `a-z`)
- Spaces
- Hyphens (`-`)
Numbers and invalid special characters are now rejected.
### Seat Format Validation
Added validation for seat numbers to enforce the required format:


## What the AI Did Well

- Generated the full data model, all five API endpoints, Pydantic validation, and SQLite schema in one pass.
- Wrote readable, well-structured seed data covering edge cases (a full/0-seat flight for the overbook test).
- Helped solve bugs and make desirable changes in the UI


## What went wrong with AI

- Wrote all 5 tests in one single file and it not runnable
- Flight search only worked with exact city names instead of partial matches (e.g., York did not return New York).
- No booking confirmation page was displayed after successfully reserving a seat.
Flight seat availability was not updating instantly after ticket cancellation and required a manual page refresh.
- Passenger name field accepted invalid characters such as numbers instead of restricting input to alphabets, spaces, and hyphens.
- Seat input field lacked format validation and did not enforce the required format (A11).