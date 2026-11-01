# Game Store QA Automation

An end-to-end QA automation project for a simple online game store, covering API testing, UI testing, test data management, and continuous integration.

## Tech Stack

- **Backend:** Python, FastAPI, SQLite
- **API Testing:** pytest, FastAPI TestClient
- **UI Testing:** Playwright, pytest
- **Test Reporting:** pytest-html
- **CI/CD:** GitHub Actions
- **Version Control:** Git, GitHub

## Features

The game store supports:

- Viewing available games and their details
- Adding games to a shopping cart
- Validating quantities and stock availability
- Handling invalid requests and unavailable products

## Automated Testing

### API Tests

14 automated tests covering:

- Game listing and game details
- Invalid game IDs
- Successful cart operations
- Invalid quantities
- Insufficient stock
- Cumulative cart quantity limits

### UI Tests

9 automated browser tests covering:

- Store page loading
- Game information display
- Successful add-to-cart operations
- Quantity validation
- Cart limits and multiple-game interactions

### Test Data Management

A pytest fixture resets the cart before each UI test through a test-only API endpoint.

The reset endpoint is enabled only when `GAME_STORE_TESTING=1`.

## Running Locally

Install project dependencies, including FastAPI, Uvicorn, pytest, HTTPX, Requests, Playwright, pytest-playwright, and pytest-html.

Install the Chromium browser:

```bash
python -m playwright install chromium
```

Run API tests:

```bash
python -m pytest tests/api/ -v
```

For UI tests, start the application in testing mode.

On Windows PowerShell:

```powershell
$env:GAME_STORE_TESTING="1"
python -m uvicorn app.main:app --reload
```

In another terminal:

```bash
python -m pytest tests/ui/ -v --browser chromium
```

## HTML Test Reports

Generate an API test report:

```bash
python -m pytest tests/api/ -v --html=report.html --self-contained-html
```

Open `report.html` in a browser to review the results.

## Continuous Integration

GitHub Actions automatically runs API and Chromium UI tests when code is pushed or a pull request is created.

The CI workflow starts the FastAPI server in testing mode before executing UI tests.

## What I Learned

- Designing and testing REST APIs
- Writing reusable pytest fixtures and parameterized tests
- Automating browser interactions with Playwright
- Managing test data with SQLite
- Debugging API responses and test failures
- Configuring GitHub Actions for continuous integration
