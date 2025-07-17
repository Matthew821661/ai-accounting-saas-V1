import csv
import io
import streamlit as st


def _to_csv(rows):
    output = io.StringIO()
    if not rows:
        return ""
    writer = csv.DictWriter(output, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def export_trial_balance(tb):
    """Expose download buttons for the trial balance."""

    if not tb:
        return

    csv_data = _to_csv(tb)
    st.download_button(
        "Download Trial Balance (CSV)", data=csv_data, file_name="trial_balance.csv"
    )
