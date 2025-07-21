"""Helpers for extracting data from invoices and matching them to bank rows.

This version avoids external dependencies so it can run in a restricted
environment.  ``extract_invoice_data_from_pdf`` simply reads the PDF file as
text and the fuzzy matching uses :mod:`difflib`.
"""

import re
from difflib import SequenceMatcher

try:  # optional dependency for better PDF parsing
    from PyPDF2 import PdfReader
    _HAS_PYPDF = True
except Exception:  # pragma: no cover - optional dependency
    _HAS_PYPDF = False

def extract_invoice_data_from_pdf(pdf_file_path):
    """Parse a PDF invoice and return basic invoice data.

    Parameters
    ----------
    pdf_file_path : str
        Path to the invoice PDF on disk.

    Returns
    -------
    dict
        Dictionary with ``amount``, ``date`` and ``supplier`` keys. Any value
        may be ``None`` if it could not be extracted.
    """

    try:
        if _HAS_PYPDF:
            reader = PdfReader(pdf_file_path)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        else:
            with open(pdf_file_path, "rb") as fh:
                data = fh.read()
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                text = data.decode("latin1", errors="ignore")
    except Exception as exc:  # pragma: no cover - I/O failures
        raise ValueError(f"Failed to read PDF '{pdf_file_path}': {exc}") from exc

    amount_match = re.search(
        r"(Total|Amount Due)\s*[:\-]?\s*R?(\d+[\.,]?\d+)", text, re.IGNORECASE
    )
    date_match = re.search(
        r"(Date|Invoice Date)\s*[:\-]?\s*(\d{2,4}[/-]\d{1,2}[/-]\d{2,4})", text
    )
    supplier_match = re.search(r"(?:From|Supplier)\s*[:\-]?\s*(\S[^\n]*)", text)

    return {
        "amount": float(amount_match.group(2).replace(",", "")) if amount_match else None,
        "date": date_match.group(2) if date_match else None,
        "supplier": supplier_match.group(1).strip() if supplier_match else "Unknown",
    }

def match_invoice_to_bank(invoice_data, bank_rows):
    """Return the best matching bank row for the provided invoice data.

    Parameters
    ----------
    invoice_data : dict
        Parsed invoice information with ``amount``, ``date`` and ``supplier`` keys.
    bank_rows : list[dict]
        List of bank statement rows, each containing ``Amount`` and ``Description``.
    """

    if not bank_rows:
        return 0, None

    matches = []
    for row in bank_rows:
        score = 0
        if invoice_data.get("amount") is not None and abs(invoice_data["amount"] - float(row.get("Amount", 0))) < 5:
            score += 40
        if invoice_data.get("supplier"):
            ratio = SequenceMatcher(None, invoice_data["supplier"].lower(), str(row.get("Description", "")).lower()).ratio()
            score += int(ratio * 50)
        if invoice_data.get("date"):
            score += 10
        matches.append((score, row))

    matches.sort(key=lambda x: x[0], reverse=True)
    return matches[0] if matches else (0, None)
