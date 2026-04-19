# Code Review Agent API

An automated Code Review Agent built as a FastAPI web service that provides structured, actionable reviews covering SOLID principles, code logic, complexity analysis, efficiency, readability, and refactoring suggestions. The agent leverages OpenAI's `gpt-4o-mini` model, enriched by static analysis tools.

## Features

- **Automated LLM Review:** Uses OpenAI's `gpt-4o-mini` to review code for SOLID principles, logic flaws, style inconsistencies, and efficiency improvements.
- **Static Analysis:** Uses `pylint` to deterministically identify syntax errors, bad practices, and code smells.
- **Complexity Analysis:** Uses `radon` to calculate Cyclomatic Complexity and the Maintainability Index.
- **Security Checking:** Integrates security analysis via Python's `bandit` to identify common vulnerabilities.
- **Downloadable Reports:** Generate detailed code review reports in both `.txt` and `.pdf` formats automatically.
- **Actionable Refactoring:** Provides before-and-after code snippets with detailed explanations for why a refactor is beneficial.

## Project Structure

```text
├── .env                  # Environment variables (e.g. OpenAI API key)
├── requirements.txt      # Project dependencies
├── app/                  
│   ├── main.py           # FastAPI application entry point
│   ├── models.py         # Pydantic models for API requests/responses
│   └── services/         # Core business logic
│       ├── orchestrator.py    # Orchestrates the review process
│       ├── llm_service.py     # Handles communication with OpenAI API
│       ├── analysis_service.py # Pylint and Radon static analysis
│       ├── security_service.py # Security analysis (Bandit)
│       └── report_service.py   # PDF/TXT report generation via fpdf
├── bad_code.py           # Sample bad code to test the API
├── test_client.py        # Python client to test the /review endpoint
└── test_improvements.py  # Script for testing advanced review parameters
```

## Prerequisites

- Python 3.8+
- An [OpenAI API Key](https://platform.openai.com/api-keys)

## Installation

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add your OpenAI API Key:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Running the Application

Start the FastAPI server using Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Alternatively:
```bash
python -m app.main
```

The API will be available at `http://localhost:8000`. You can also view the interactive Swagger API documentation at `http://localhost:8000/docs`.

## API Endpoints

### 1. Code Review Analysis
* **Endpoint:** `POST /review`
* **Description:** Analyzes the provided source code for issues, complexity, and refactoring insights.
* **Request Body (JSON):**
  ```json
  {
    "code": "def foo(): pass",
    "language": "python",
    "filename": "optional_filename.py"
  }
  ```
* **Response (JSON):** Returns an object containing `issues`, `complexity`, `efficiency_recommendations`, `style_suggestions`, and `refactoring_suggestions`.

### 2. Generate Downloadable Report
* **Endpoint:** `POST /review/report?format={txt|pdf}`
* **Description:** Generates a downloadable review report based on the provided code.
* **Query Parameter:** `format` (either `txt` or `pdf` - defaults to `txt`).
* **Request Body:** Same JSON structure as `/review`.
* **Response:** File streaming response (`application/octet-stream`) containing the report.

### 3. Server Health Check
* **Endpoint:** `GET /health`
* **Description:** Used to check if the API is up and running.
* **Response:** `{"status": "healthy"}`

## Testing the API Locally

You can use the provided client scripts to test out the application with the included sample code:

1. Test the standard review endpoint:
   ```bash
   python test_client.py
   ```
   This script reads `bad_code.py` and posts it to the `/review` endpoint, and prints out the formatted JSON output.

2. Test additional evaluation techniques:
   ```bash
   python test_improvements.py
   ```
