"""Utility helpers to export financial reports."""

import io
import streamlit as st
import pandas as pd

def export_trial_balance(tb: pd.DataFrame) -> None:
    """Render download buttons for a trial balance DataFrame.

    Parameters
    ----------
    tb:
        The trial balance to export.
    """

    # Export Excel version
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        tb.to_excel(writer, index=False)
    excel_buffer.seek(0)
    st.download_button(
        label="Download Trial Balance (Excel)",
        data=excel_buffer.getvalue(),
        file_name="trial_balance.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    # Export CSV version
    csv_buffer = io.StringIO()
    tb.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue().encode("utf-8")
    st.download_button(
        label="Download Trial Balance (CSV)",
        data=csv_bytes,
        file_name="trial_balance.csv",
        mime="text/csv",
    )


