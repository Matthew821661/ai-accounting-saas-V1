import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.invoice_matcher import match_invoice_to_bank


def test_match_invoice_to_bank_best_row():
    bank_rows = [
        {"Description": "MTN Data", "Amount": 100.0},
        {"Description": "Other", "Amount": 50.0},
    ]
    invoice = {"amount": 100.0, "supplier": "MTN", "date": "2023-01-01"}
    score, row = match_invoice_to_bank(invoice, bank_rows)
    assert row["Description"] == "MTN Data"
    assert score > 0

