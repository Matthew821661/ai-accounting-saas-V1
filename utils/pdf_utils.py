import io
import csv
import re


def extract_text(pdf_file_path, ocr=False):
    """Return text from a PDF file. If ``ocr`` is True and pytesseract is
    available, it will attempt OCR after converting pages to images.
    """
    text = ""
    if ocr:
        try:
            from pdf2image import convert_from_path  # pragma: no cover - optional
            import pytesseract  # pragma: no cover - optional

            images = convert_from_path(pdf_file_path)
            text = "\n".join(pytesseract.image_to_string(img) for img in images)
        except Exception:
            text = ""

    if not text.strip():
        try:
            from PyPDF2 import PdfReader  # pragma: no cover - optional

            reader = PdfReader(pdf_file_path)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception:
            try:
                with open(pdf_file_path, "rb") as fh:
                    data = fh.read()
                text = data.decode("utf-8")
            except Exception:
                with open(pdf_file_path, "rb") as fh:
                    data = fh.read()
                text = data.decode("latin1", errors="ignore")
    return text


def parse_bank_statement_pdf(pdf_file_path):
    """Parse a bank statement PDF and return a list of row dictionaries."""
    text = extract_text(pdf_file_path, ocr=True)
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            parts = next(csv.reader([line]))
        except Exception:
            parts = re.split(r"\s{2,}", line)
        if len(parts) >= 3:
            date, desc, amount = parts[0].strip(), parts[1].strip(), parts[2].strip()
            rows.append({"Date": date, "Description": desc, "Amount": amount})
    return rows
