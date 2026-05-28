# ParaBank E2E Automation Framework

End-to-end UI automation project built with `pytest` and Playwright against the public ParaBank demo banking site.

This project is structured as a small but realistic automation framework rather than a single test file. It uses reusable page objects, generated test data, shared fixtures, environment-based configuration, failure screenshots, and both positive and negative end-to-end scenarios.

## What This Project Covers

- Public navigation flows
- About, Services, and Site Map page checks
- Home page layout and navigation checks
- Contact, registration, and customer lookup form visibility checks
- Contact form submission
- Required-field validation for contact form
- User registration
- Required-field validation for registration
- Logout after registration
- Empty login validation
- Duplicate username validation
- Forgot-login recovery
- Customer lookup failure handling
- Internal ParaBank error detection so tests do not pass when the site renders server errors

## Tech Stack

- Python
- Pytest
- Playwright
- Allure Report
- Page Object Model
- Environment-based configuration with `.env`

## Framework Highlights

- Shared Playwright fixtures in [conftest.py](./conftest.py)
- Centralized runtime settings in [src/core/settings.py](./src/core/settings.py)
- Allure reporting helpers in [src/core/reporting.py](./src/core/reporting.py)
- Reusable generated data in [src/core/test_data.py](./src/core/test_data.py)
- Page-object implementation in [src/pages/parabank_page.py](./src/pages/parabank_page.py)
- One focused scenario per test file under [tests](./tests)
- Automatic screenshots on test failure
- Allure result generation with readable steps, environment metadata, and failure screenshot attachments
- Headed local execution with slow motion, maximized browser, and a 5-second pause between tests
- Guard assertions that fail fast if ParaBank displays its internal server-error panel

## Run Locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
pytest -q tests
```

The default pytest configuration writes Allure results into `allure-results/`.

Run only the positive demo flow if you want browser screenshots without red validation messages:

```powershell
pytest -q tests -m "not negative"
```

Run only validation/rejection checks:

```powershell
pytest -q tests -m negative
```

## Allure Report

Install the dependencies first:

```powershell
python -m pip install -r requirements.txt
```

Run the tests and generate fresh Allure results:

```powershell
pytest -q tests
```

Open the interactive Allure report:

```powershell
allure.cmd serve allure-results
```

Or generate a static report folder:

```powershell
allure.cmd generate allure-results -o allure-report --clean
allure.cmd open allure-report
```

Allure CLI and Java must be installed separately on the machine to open the HTML report. The pytest run still creates raw `allure-results/` even if the CLI is not installed.

On Windows, common install options include Scoop, Chocolatey, or Node.js/npm. Example with npm after Node.js is installed:

```powershell
npm install -g allure-commandline
```

If PowerShell blocks `allure` because of script execution policy, use `allure.cmd` as shown above.

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
|   |   |-- reporting.py
|   |   |-- settings.py
|   |   `-- test_data.py
|   `-- pages
|       |-- base_page.py
|       `-- parabank_page.py
`-- tests
    |-- conftest.py
    |-- test_about_page_disclaimer.py
    |-- test_contact_form_fields_visible.py
    |-- test_contact_form_required_fields.py
    |-- test_contact_form_submission.py
    |-- test_customer_lookup_failure.py
    |-- test_customer_lookup_form_fields_visible.py
    |-- test_customer_lookup_recovers_registered_user.py
    |-- test_duplicate_username_validation.py
    |-- test_empty_login_requires_credentials.py
    |-- test_home_page_layout.py
    |-- test_registration_form_fields_visible.py
    |-- test_registration_success.py
    |-- test_registration_required_fields.py
    |-- test_services_page_lists_bookstore_services.py
    `-- test_site_map_lists_account_services.py
```

## Notes

- The target system is an external public demo site, so behavior can change outside the project.
- Red field-validation messages are expected in tests marked `negative`; they confirm the site rejects invalid input correctly.
- ParaBank currently renders internal server errors on several logged-in banking flows, including accounts overview, opening new accounts, account details, bill pay, profile updates, loans, and transaction search. Those flows are intentionally excluded from the default demo suite so the visible run stays clean and trustworthy.
- Failed tests save screenshots into `artifacts/screenshots/`.
- The suite is intended to fail if ParaBank displays `An internal error has occurred and has been logged.`
