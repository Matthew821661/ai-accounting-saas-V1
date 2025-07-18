import streamlit as st
import pandas as pd
import io

def export_trial_balance(tb):
    """Offer trial balance for download in Excel and CSV formats."""

    # Create an in-memory Excel file rather than relying on the return
    # value of ``DataFrame.to_excel`` (which is always ``None``).
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        tb.to_excel(writer, index=False)
    excel_buffer.seek(0)

    st.download_button(
        "Download Trial Balance (Excel)",
        data=excel_buffer.read(),
        file_name="trial_balance.xlsx",
    )

    st.download_button(
        "Download Trial Balance (CSV)",
        data=tb.to_csv(index=False).encode("utf-8"),
        file_name="trial_balance.csv",
    )
