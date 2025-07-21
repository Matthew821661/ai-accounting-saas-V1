import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.classifier import classify_transaction


def test_classifier_examples():
    assert classify_transaction("MTN data purchase") == "6100/000 - Telecoms Expense"
    assert classify_transaction("Salary payment for June") == "5000/000 - Payroll"
    assert classify_transaction("Invoice 001 for services") == "4000/000 - Sales"
    assert classify_transaction("ATM withdrawal") == "1000/000 - Cash"
