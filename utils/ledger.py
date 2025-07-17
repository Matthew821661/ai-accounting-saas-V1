def generate_ledger(bank_df):
    bank_df["GL Account"] = bank_df["Description"].apply(lambda x: "6100/000 - Expense" if "MTN" in str(x).upper() else "1000/000 - Cash")
    bank_df["Debit"] = bank_df["Amount"].apply(lambda x: x if x > 0 else 0)
    bank_df["Credit"] = bank_df["Amount"].apply(lambda x: -x if x < 0 else 0)
    return bank_df
