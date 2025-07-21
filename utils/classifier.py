"""Simple transaction classifier used as a stand-in for an AI model."""


def classify_transaction(description):
    desc = str(description).lower()
    if "mtn" in desc or "tel" in desc:
        return "6100/000 - Telecoms Expense"
    if "salary" in desc or "payroll" in desc:
        return "5000/000 - Payroll"
    if "invoice" in desc or "sale" in desc or "customer" in desc:
        return "4000/000 - Sales"
    return "1000/000 - Cash"
