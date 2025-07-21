import io
import csv
import re


def parse_bank_statement_csv(csv_text):
    """Parse CSV text and return a list of bank rows.

    Raises
    ------
    ValueError
        If the CSV is malformed or missing required columns.
    """
    try:
        reader = csv.DictReader(io.StringIO(csv_text))
    except csv.Error as exc:  # pragma: no cover - csv failures
        raise ValueError(f"Invalid CSV format: {exc}") from exc

    rows = list(reader)
    if not rows:
        raise ValueError("CSV file contained no rows")

    required = {"Description", "Amount"}
    missing = required - set(reader.fieldnames or [])
    if missing:
        raise ValueError(f"CSV missing required columns: {', '.join(sorted(missing))}")

    return rows


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
    if not text.strip():
        raise ValueError("No text could be extracted from the PDF")

    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            parts = next(csv.reader([line]))
        except Exception:
            parts = re.split(r"\s{2,}|\t+", line)
        if len(parts) < 3:
            match = re.match(r"(\d{2}/\d{2}/\d{4})\s+(.*?)\s+(-?\d[\d,\.]*?)$", line)
            if match:
                parts = [match.group(1), match.group(2), match.group(3)]
        if len(parts) >= 3:
            date, desc, amount = parts[0].strip(), parts[1].strip(), parts[2].strip()
            amount = amount.replace("R", "").replace(",", "")
            rows.append({"Date": date, "Description": desc, "Amount": amount})

    if not rows:
        raise ValueError("Could not parse any transaction rows from PDF")

    return rows
