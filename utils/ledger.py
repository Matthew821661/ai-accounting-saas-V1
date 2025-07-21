from .classifier import classify_transaction


def generate_ledger(bank_rows):
    """Create a rudimentary general ledger from a bank statement.

    The GL account for each transaction is determined using a simple
    classifier which acts as a lightweight stand-in for an AI model.
    """

    if not bank_rows:
        return bank_rows

    ledger = []
    for row in bank_rows:
        entry = row.copy()
        entry["GL Account"] = classify_transaction(row.get("Description", ""))
        try:
            amount = float(str(row.get("Amount", 0)).replace(",", ""))
        except ValueError:
            amount = 0
        entry["Debit"] = amount if amount > 0 else 0
        entry["Credit"] = -amount if amount < 0 else 0
        ledger.append(entry)
    return ledger
