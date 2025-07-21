import io
import os
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.pdf_utils import extract_text, parse_bank_statement_pdf


def test_extract_text_reads_plain_file(tmp_path):
    pdf_path = tmp_path / "sample.pdf"
    pdf_path.write_text("hello world")
    text = extract_text(str(pdf_path))
    assert text.strip() == "hello world"


def test_parse_bank_statement_pdf_mixed_formats(tmp_path):
    content = "2023-01-01,MTN,100\n2023-01-02,Other,50\n"
    pdf_path = tmp_path / "statement.pdf"
    pdf_path.write_text(content)
    rows = parse_bank_statement_pdf(str(pdf_path))
    assert rows == [
        {"Date": "2023-01-01", "Description": "MTN", "Amount": "100"},
        {"Date": "2023-01-02", "Description": "Other", "Amount": "50"},
    ]
