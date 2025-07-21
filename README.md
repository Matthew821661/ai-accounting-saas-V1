# AI Accounting SaaS

This project is a small prototype of a bookkeeping application built with [Streamlit](https://streamlit.io/). It demonstrates how invoices can be matched to bank statement transactions and how a general ledger and trial balance can be produced.

## Features

- Upload bank statements in CSV **or PDF** format (basic OCR support)
- Parse invoice PDFs and match them to transactions
- Classify transactions into GL accounts using a lightweight classifier
- Generate a simple general ledger and trial balance
- Download the trial balance and general ledger as CSV, with optional PDF/Excel export if dependencies are installed

## Installation

1. Install Python 3.8+.
2. Install the project dependencies:
   ```bash
   pip install -r requirements.txt
   # Optional: install extra libraries for better PDF parsing and exports
   pip install PyPDF2 pdf2image pytesseract pandas fpdf
   ```
   The `requirements.txt` file includes `pytest` so you can run the test suite.

## Setup

The app expects no special environment variables by default. If you wish to
customize things like the Streamlit port or enable additional PDF/Excel
functionality you can create a `.env` file and set environment variables before
running the app.

## Deployment

You can deploy the prototype using Docker. Build the image from the repository
root and then run a container exposing port `8501`:

```bash
docker build -t ai-accounting-saas .
docker run -p 8501:8501 ai-accounting-saas
```

Visit `http://localhost:8501` in your browser to access the app.

## Usage

Run the Streamlit app from the repository root (requires `streamlit`):

```bash
streamlit run app/main.py
```

A login form will appear. Authentication is only a demo – any credentials will work. After logging in you can upload a bank statement and invoices to see the matching in action.

## Running Tests

Unit tests live in the `tests` directory and can be executed with `pytest`:

```bash
pytest
```

## Repository Layout

```
app/                # Streamlit entry point
components/         # UI components
utils/              # Helper functions for matching and accounting
```

This is an experimental prototype and not production-ready. Contributions are welcome!

## Security Notes

Authentication in this project is only a placeholder and **should not** be used
to protect sensitive data. There is no encryption or database layer, so run the
application in a trusted environment only.

