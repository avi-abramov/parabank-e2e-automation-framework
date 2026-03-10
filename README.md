# ParaBank E2E Automation Framework

End-to-end UI automation project built with `pytest` and Playwright against the public ParaBank demo banking site.

This project is structured as a small but realistic automation framework rather than a single test file. It uses reusable page objects, generated test data, shared fixtures, environment-based configuration, failure screenshots, and both positive and negative end-to-end scenarios.

## What This Project Covers

- Public navigation flows
- Contact form submission
- User registration
- Login and logout
- Invalid login handling
- Duplicate username validation
- Forgot-login recovery
- Customer lookup failure handling
- Open new account
- Transfer funds between accounts
- Account details and transaction history
- Bill pay
- Update contact information
- Loan request
- Transaction lookup by date

## Tech Stack

- Python
- Pytest
- Playwright
- Page Object Model
- Environment-based configuration with `.env`

## Framework Highlights

- Shared Playwright fixtures in [conftest.py](./conftest.py)
- Centralized runtime settings in [src/core/settings.py](./src/core/settings.py)
- Reusable generated data in [src/core/test_data.py](./src/core/test_data.py)
- Page-object implementation in [src/pages/parabank_page.py](./src/pages/parabank_page.py)
- End-to-end suite in [tests/test_parabank_e2e.py](./tests/test_parabank_e2e.py)
- Automatic screenshots on test failure
- Headed local execution with slow motion, maximized browser, and a 5-second pause between tests

## Run Locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
pytest -q tests/test_parabank_e2e.py
```

## Default Local Run Behavior

The local configuration is intentionally set for demonstration:

- `HEADLESS=false`
- `START_MAXIMIZED=true`
- `SLOW_MO_MS=600`
- `TEST_PAUSE_MS=5000`

That means the browser opens visibly, starts maximized, performs actions more slowly, and pauses 5 seconds between tests.

## Configuration

Copy `.env.example` to `.env` and adjust values if needed.

```env
BASE_URL=https://parabank.parasoft.com/parabank/
BROWSER=chromium
HEADLESS=false
START_MAXIMIZED=true
SLOW_MO_MS=600
VIEWPORT_WIDTH=1440
VIEWPORT_HEIGHT=900
DEFAULT_TIMEOUT_MS=10000
TEST_PAUSE_MS=5000
```

## Project Structure

```text
.
|-- conftest.py
|-- pytest.ini
|-- requirements.txt
|-- src
|   |-- core
|   |   |-- fixtures.py
|   |   |-- settings.py
|   |   `-- test_data.py
|   `-- pages
|       |-- base_page.py
|       `-- parabank_page.py
`-- tests
    `-- test_parabank_e2e.py
```

## Notes

- The target system is an external public demo site, so behavior can change outside the project.
- Failed tests save screenshots into `artifacts/screenshots/`.
- The current suite was verified successfully in both fast headless validation mode and visible demo mode.
