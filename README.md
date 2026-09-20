# E-Commerce API & Database QA Automation Framework

A Python-based QA automation framework for validating REST API behavior and verifying data persistence in SQLite.

## Project Goals

This project demonstrates:

- REST API functional testing
- Positive and negative test scenarios
- HTTP status-code and response validation
- Database persistence validation
- Reusable pytest fixtures
- Automated HTML test reporting
- CI-ready test execution

## Technology Stack

- Python 3
- Pytest
- Requests
- Flask
- SQLite
- SQL
- pytest-html
- GitHub Actions

## Test Flow

```text
Test Case
   ↓
API Request
   ↓
Response Validation
   ↓
SQLite Data Validation
   ↓
Pytest Assertions
   ↓
HTML Test Report
```

## Recommended Project Structure

```text
.
├── app/
│   └── ...
├── tests/
│   ├── api/
│   ├── database/
│   └── conftest.py
├── utils/
│   ├── api_client.py
│   └── database_client.py
├── requirements.txt
├── pytest.ini
└── README.md
```

## Installation

```bash
git clone <repository-url>
cd API-DB-QA-Automation

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Running the Tests

Run all tests:

```bash
pytest
```

Generate an HTML report:

```bash
pytest --html=reports/test-report.html --self-contained-html
```

Run a specific test group:

```bash
pytest tests/api
pytest tests/database
```

## Coverage

```bash
pytest --cov=. --cov-report=term-missing
```

Add the actual coverage percentage here after running the test suite.

## Test Coverage

The framework should cover:

- Valid product creation and retrieval
- Invalid request payloads
- Required-field validation
- Duplicate records
- Invalid resource identifiers
- HTTP status-code validation
- Response schema validation
- Database record persistence
- Update and delete consistency
- Empty and boundary-value inputs

## Quality Practices

- Reusable API and database clients
- Pytest fixtures for setup and cleanup
- Environment-based configuration
- Explicit request timeouts
- Meaningful assertions and failure messages
- Isolated test data
- Automated test reports
- CI execution through GitHub Actions

## Example Test Result

Add a real result after execution:

```text
XX passed, X failed
Coverage: XX%
HTML report: reports/test-report.html
```

## Resume Summary

> Developed a Python/Pytest QA automation framework for testing REST APIs and validating SQLite database persistence. Implemented reusable API and database utilities, positive and negative test scenarios, HTTP response validation, database integrity checks, and automated HTML test reporting.

## Project Status

This project is actively being improved with additional API coverage, database validation, reporting, and CI automation.
