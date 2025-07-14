import streamlit as st
from utils.invoice_matcher import extract_invoice_data_from_pdf, match_invoice_to_bank
import tempfile
import pandas as pd

def run_invoice_matcher(bank_df):
    st.subheader("Upload Invoice (PDF)")
    uploaded_invoice = st.file_uploader("Invoice PDF", type=["pdf"])
    if uploaded_invoice and bank_df is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_invoice.read())
            invoice_data = extract_invoice_data_from_pdf(tmp.name)
        st.write("Extracted Invoice Data", invoice_data)

        score, matched_row = match_invoice_to_bank(invoice_data, bank_df)
        if matched_row is not None:
            st.success(f"Best Match Found (Score: {score})")
            st.dataframe(pd.DataFrame([matched_row]))
        else:
            st.warning("No suitable match found.")