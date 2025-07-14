import pdfplumber
import re
from rapidfuzz import fuzz

def extract_invoice_data_from_pdf(pdf_file_path):
    with pdfplumber.open(pdf_file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    amount_match = re.search(r"(Total|Amount Due)\s*[:\-]?\s*R?(\d+[\.,]?\d+)", text, re.IGNORECASE)
    date_match = re.search(r"(Date|Invoice Date)\s*[:\-]?\s*(\d{2,4}[/-]\d{1,2}[/-]\d{2,4})", text)
    supplier_match = re.search(r"(From|Supplier)\s*[:\-]?\s*(.*)", text)

    return {
        "amount": float(amount_match.group(2).replace(',', '')) if amount_match else None,
        "date": date_match.group(2) if date_match else None,
        "supplier": supplier_match.group(2).strip() if supplier_match else "Unknown"
    }

def match_invoice_to_bank(invoice_data, bank_df):
    matches = []
    for _, row in bank_df.iterrows():
        score = 0
        if invoice_data["amount"] and abs(invoice_data["amount"] - row["Amount"]) < 5:
            score += 40
        if invoice_data["supplier"]:
            score += int(fuzz.partial_ratio(invoice_data["supplier"].lower(), str(row["Description"]).lower()) * 0.5)
        if invoice_data["date"]:
            score += 10
        matches.append((score, row))
    matches.sort(key=lambda x: x[0], reverse=True)
    return matches[0] if matches else (0, None)