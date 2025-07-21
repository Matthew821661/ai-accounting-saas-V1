"""Utility helpers for exporting accounting data."""

import csv
import io
import streamlit as st


def _to_excel(rows):
    """Return an XLSX bytes object for the rows if pandas is available."""
    try:
        import pandas as pd  # pragma: no cover - optional dependency

        df = pd.DataFrame(rows)
        output = io.BytesIO()
        df.to_excel(output, index=False)
        return output.getvalue()
    except Exception:  # pragma: no cover - optional dependency
        return None


def _to_pdf(rows, title):
    """Return a PDF bytes object for the rows if FPDF is available."""
    try:
        from fpdf import FPDF  # pragma: no cover - optional dependency

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=title, ln=1)
        headers = list(rows[0].keys()) if rows else []
        for row in rows:
            line = " | ".join(str(row.get(h, "")) for h in headers)
            pdf.cell(200, 10, txt=line, ln=1)
        return pdf.output(dest="S").encode("latin1")
    except Exception:  # pragma: no cover - optional dependency
        return None


def _to_csv(rows):
    """Return a CSV string for the provided row dictionaries."""

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

    pdf_data = _to_pdf(tb, "Trial Balance")
    if pdf_data:
        st.download_button(
            "Download Trial Balance (PDF)",
            data=pdf_data,
            file_name="trial_balance.pdf",
        )

    excel_data = _to_excel(tb)
    if excel_data:
        st.download_button(
            "Download Trial Balance (Excel)",
            data=excel_data,
            file_name="trial_balance.xlsx",
        )


def export_general_ledger(gl_rows):
    """Expose download buttons for the general ledger."""

    if not gl_rows:
        return

    csv_data = _to_csv(gl_rows)
    st.download_button(
        "Download General Ledger (CSV)", data=csv_data, file_name="general_ledger.csv"
    )

    pdf_data = _to_pdf(gl_rows, "General Ledger")
    if pdf_data:
        st.download_button(
            "Download General Ledger (PDF)",
            data=pdf_data,
            file_name="general_ledger.pdf",
        )

    excel_data = _to_excel(gl_rows)
    if excel_data:
        st.download_button(
            "Download General Ledger (Excel)",
            data=excel_data,
            file_name="general_ledger.xlsx",
        )
