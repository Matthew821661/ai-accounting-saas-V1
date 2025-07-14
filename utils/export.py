import streamlit as st

def export_trial_balance(tb):
    st.download_button("Download Trial Balance (Excel)", tb.to_excel(index=False), file_name="trial_balance.xlsx")
    st.download_button("Download Trial Balance (CSV)", tb.to_csv(index=False), file_name="trial_balance.csv")