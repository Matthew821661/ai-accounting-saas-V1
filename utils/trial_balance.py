def generate_trial_balance(gl_rows):
    """Aggregate debits and credits per GL account."""

    if not gl_rows:
        return gl_rows

    totals = {}
    for row in gl_rows:
        account = row.get("GL Account")
        if account not in totals:
            totals[account] = {"GL Account": account, "Debit": 0, "Credit": 0}
        totals[account]["Debit"] += float(row.get("Debit", 0))
        totals[account]["Credit"] += float(row.get("Credit", 0))

    return list(totals.values())
