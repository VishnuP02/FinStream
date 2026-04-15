import numpy as np

_MODEL = None

CATEGORY_MAP = {
    "retail": 0,
    "gas": 1,
    "electronics": 2,
    "travel": 3,
    "cash": 4,
    "transfer": 5,
    "crypto": 6,
}

TYPE_MAP = {
    "debit_card": 0,
    "credit_card": 1,
    "atm": 2,
    "wire": 3,
    "international": 4,
    "crypto_transfer": 5,
}

TRUSTED_LOCATIONS = {
    "philadelphia, pa",
    "wilmington, de",
    "newark, de",
    "horsham, pa",
    "abington, pa",
}


def _feature_vector(amount: float, merchant_category: str, transaction_type: str, location: str):
    category_code = CATEGORY_MAP.get(merchant_category.lower().strip(), 99)
    type_code = TYPE_MAP.get(transaction_type.lower().strip(), 99)
    is_untrusted_location = 0 if location.lower().strip() in TRUSTED_LOCATIONS else 1

    return np.array([[amount, category_code, type_code, is_untrusted_location]], dtype=float)


def _build_training_data():
    training_examples = [
        (45.00, "Gas", "debit_card", "Wilmington, DE", 0),
        (89.99, "Retail", "credit_card", "Philadelphia, PA", 0),
        (19.55, "Travel", "credit_card", "Philadelphia, PA", 0),
        (124.99, "Retail", "debit_card", "Philadelphia, PA", 0),
        (58.10, "Gas", "debit_card", "Horsham, PA", 0),
        (250.00, "Retail", "credit_card", "Abington, PA", 0),
        (500.00, "Cash", "atm", "Baltimore, MD", 1),
        (1299.99, "Electronics", "credit_card", "Newark, DE", 1),
        (6200.00, "Transfer", "wire", "London, UK", 1),
        (4500.00, "Travel", "international", "Dubai, UAE", 1),
        (7800.00, "Crypto", "crypto_transfer", "Unknown", 1),
        (1400.00, "Electronics", "credit_card", "Chicago, IL", 1),
    ]

    X = []
    y = []

    for amount, category, txn_type, location, label in training_examples:
        X.append(_feature_vector(amount, category, txn_type, location)[0])
        y.append(label)

    return np.array(X, dtype=float), np.array(y, dtype=int)


def _get_model():
    global _MODEL
    if _MODEL is None:
        from sklearn.linear_model import LogisticRegression

        X_train, y_train = _build_training_data()
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)
        _MODEL = model
    return _MODEL


def predict_ml_fraud_score(transaction) -> float:
    model = _get_model()
    features = _feature_vector(
        transaction.amount,
        transaction.merchant_category,
        transaction.transaction_type,
        transaction.location,
    )
    probability = model.predict_proba(features)[0][1]
    return round(float(probability), 2)