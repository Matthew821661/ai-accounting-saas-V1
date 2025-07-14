import streamlit as st
import pandas as pd
from components.invoice_matcher_ui import run_invoice_matcher
from utils.ledger import generate_ledger
from utils.trial_balance import generate_trial_balance
from utils.export import export_trial_balance

def launch_dashboard(session):
    st.title("AI Bookkeeping Dashboard")
    st.success(f"Welcome {session['user']['email']}")

    st.subheader("Upload Bank Statement")
    bank_file = st.file_uploader("Bank Statement (.xlsx)", type=["xlsx"])
    bank_df = None
    if bank_file:
        bank_df = pd.read_excel(bank_file)
        st.write("Transactions")
        st.dataframe(bank_df)

    run_invoice_matcher(bank_df)

    if bank_df is not None:
        gl = generate_ledger(bank_df)
        st.subheader("General Ledger")
        st.dataframe(gl)

        tb = generate_trial_balance(gl)
        st.subheader("Trial Balance")
        st.dataframe(tb)

        export_trial_balance(tb)