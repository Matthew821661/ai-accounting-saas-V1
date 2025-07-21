import os
import tempfile
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.pdf_utils import parse_bank_statement_csv, parse_bank_statement_pdf


def test_parse_bank_statement_csv_missing_columns():
    csv_text = "Date,Amount\n2023-01-01,100"
    try:
        parse_bank_statement_csv(csv_text)
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "missing required columns" in str(exc)


def test_parse_bank_statement_pdf_invalid(tmp_path):
    # create a fake pdf file with garbage content
    fake_pdf = tmp_path / "bad.pdf"
    fake_pdf.write_text("not a real pdf")
    try:
        parse_bank_statement_pdf(str(fake_pdf))
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "Could not" in str(exc) or "No text" in str(exc)
