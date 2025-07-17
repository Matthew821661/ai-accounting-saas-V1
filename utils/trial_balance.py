def generate_trial_balance(gl_df):
    tb = (
        gl_df.groupby("GL Account").agg({"Debit": "sum", "Credit": "sum"}).reset_index()
    )
    return tb
