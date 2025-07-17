import tempfile
import streamlit as st

from utils.invoice_matcher import extract_invoice_data_from_pdf, match_invoice_to_bank

def run_invoice_matcher(bank_rows):
    """UI widget for uploading an invoice and displaying the match."""

    st.subheader("Upload Invoice (PDF)")
    uploaded_invoice = st.file_uploader("Invoice PDF", type=["pdf"])

    if uploaded_invoice and bank_rows:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_invoice.read())
            try:
                invoice_data = extract_invoice_data_from_pdf(tmp.name)
            except Exception as exc:
                st.error(f"Failed to process invoice: {exc}")
                return
        st.write("Extracted Invoice Data", invoice_data)

        score, matched_row = match_invoice_to_bank(invoice_data, bank_rows)
        if matched_row is not None:
            st.success(f"Best Match Found (Score: {score})")
            st.table([matched_row])
        else:
            st.warning("No suitable match found.")
