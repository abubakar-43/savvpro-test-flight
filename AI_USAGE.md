# AI Usage

## Tool Used

**Claude Sonnet**


## Prompts

1. **Initial scaffold**  
The AI was given the full specification with 5 defined tests and it produced all code, tests, and documentation files iteratively, fixing issues as they arose.


## What the AI Did Well

- Generated the full data model, all five API endpoints, Pydantic validation, and SQLite schema in one pass.
- Wrote readable, well-structured seed data covering edge cases (a full/0-seat flight for the overbook test).

## What went wrong with AI
- Wrote all 5 tests in one single file and it not runnable