import csv
import io
import os
import tempfile
import streamlit as st
from components.invoice_matcher_ui import run_invoice_matcher
from utils.ledger import generate_ledger
from utils.trial_balance import generate_trial_balance
from utils.export import export_trial_balance, export_general_ledger
from utils.pdf_utils import parse_bank_statement_pdf

def launch_dashboard(session):
    """Main dashboard screen shown after login."""

    st.title("AI Bookkeeping Dashboard")
    st.success(f"Welcome {session['user']['email']}")

    st.subheader("Upload Bank Statement")
    bank_file = st.file_uploader("Bank Statement (.csv or .pdf)", type=["csv", "pdf"])
    bank_rows = []
    if bank_file:
        try:
            if bank_file.type == "application/pdf" or bank_file.name.lower().endswith(".pdf"):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(bank_file.read())
                    tmp_path = tmp.name
                bank_rows = parse_bank_statement_pdf(tmp_path)
                os.unlink(tmp_path)
            else:
                content = bank_file.getvalue().decode("utf-8", errors="ignore")
                reader = csv.DictReader(io.StringIO(content))
                bank_rows = list(reader)
            st.write("Transactions")
            st.table(bank_rows)
        except Exception as exc:
            st.error(f"Failed to read bank statement: {exc}")

    run_invoice_matcher(bank_rows)

    if bank_rows:
        gl = generate_ledger(bank_rows)
        st.subheader("General Ledger")
        st.table(gl)

        tb = generate_trial_balance(gl)
        st.subheader("Trial Balance")
        st.table(tb)

        export_general_ledger(gl)
        export_trial_balance(tb)
