def generate_ledger(bank_rows):
    """Create a rudimentary general ledger from a bank statement."""

    if not bank_rows:
        return bank_rows

    ledger = []
    for row in bank_rows:
        entry = row.copy()
        entry["GL Account"] = (
            "6100/000 - Expense" if "MTN" in str(row.get("Description", "")).upper() else "1000/000 - Cash"
        )
        try:
            amount = float(str(row.get("Amount", 0)).replace(",", ""))
        except ValueError:
            amount = 0
        entry["Debit"] = amount if amount > 0 else 0
        entry["Credit"] = -amount if amount < 0 else 0
        ledger.append(entry)
    return ledger
