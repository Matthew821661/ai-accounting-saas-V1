# AI Accounting SaaS

This project is a small prototype of a bookkeeping application built with [Streamlit](https://streamlit.io/). It demonstrates how invoices can be matched to bank statement transactions and how a general ledger and trial balance can be produced.

## Features

- Upload bank statements in CSV format
- Parse invoice PDFs and match them to transactions
- Generate a simple general ledger and trial balance
- Download the trial balance as CSV

## Installation

1. Install Python 3.8+.
2. Install the project dependencies:
   ```bash
   pip install -r requirements.txt
   # Optional: install PyPDF2 for better invoice parsing
   pip install PyPDF2
   ```
   The `requirements.txt` file includes `pytest` so you can run the test suite.

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

