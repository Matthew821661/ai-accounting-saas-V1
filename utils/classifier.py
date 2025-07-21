"""Tiny ML-based transaction classifier.

This module now trains a very small logistic regression model on some
sample transactions.  It acts as a lightweight replacement for the
previous keyword-based logic while still remaining simple and fast.
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression


# Minimal labelled data used to train the classifier.  The examples are
# intentionally tiny; they merely provide enough signal for the tests to
# verify that the model works end-to-end.
_TRAIN_DATA = [
    ("mtn airtime", "6100/000 - Telecoms Expense"),
    ("telkom data bundle", "6100/000 - Telecoms Expense"),
    ("telephone bill", "6100/000 - Telecoms Expense"),
    ("monthly salary", "5000/000 - Payroll"),
    ("payroll payment", "5000/000 - Payroll"),
    ("employee wages", "5000/000 - Payroll"),
    ("customer invoice", "4000/000 - Sales"),
    ("product sale", "4000/000 - Sales"),
    ("sales receipt", "4000/000 - Sales"),
    ("atm withdrawal", "1000/000 - Cash"),
    ("cash deposit", "1000/000 - Cash"),
    ("other expense", "1000/000 - Cash"),
]


_VECTORIZER = CountVectorizer(lowercase=True)
_X_TRAIN = _VECTORIZER.fit_transform([d for d, _ in _TRAIN_DATA])
_Y_TRAIN = [label for _, label in _TRAIN_DATA]

_MODEL = LogisticRegression(max_iter=200)
_MODEL.fit(_X_TRAIN, _Y_TRAIN)


def classify_transaction(description: str) -> str:
    """Classify a transaction description into a GL account string."""

    vector = _VECTORIZER.transform([str(description)])
    return _MODEL.predict(vector)[0]
