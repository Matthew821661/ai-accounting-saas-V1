import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.ledger import generate_ledger
from utils.trial_balance import generate_trial_balance


def test_generate_ledger_basic():
    rows = [{"Description": "MTN Data", "Amount": "100"}, {"Description": "Other", "Amount": "-50"}]
    ledger = generate_ledger(rows)
    assert ledger[0]["GL Account"].startswith("6100")
    assert ledger[0]["Debit"] == 100
    assert ledger[1]["Credit"] == 50


def test_generate_trial_balance_totals():
    rows = [
        {"GL Account": "1000/000 - Cash", "Debit": 100, "Credit": 0},
        {"GL Account": "1000/000 - Cash", "Debit": 0, "Credit": 20},
    ]
    tb = generate_trial_balance(rows)
    assert tb[0]["Debit"] == 100
    assert tb[0]["Credit"] == 20
