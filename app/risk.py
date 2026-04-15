def calculate_fraud_score(transaction) -> tuple[float, list[str]]:
    score = 0.0
    reasons = []

    high_risk_categories = {"electronics", "cash", "travel", "crypto", "transfer"}
    high_risk_types = {"wire", "atm", "international", "crypto_transfer"}
    trusted_locations = {
        "philadelphia, pa",
        "wilmington, de",
        "newark, de",
        "horsham, pa",
        "abington, pa",
    }

    category = transaction.merchant_category.lower().strip()
    txn_type = transaction.transaction_type.lower().strip()
    location = transaction.location.lower().strip()

    if transaction.amount >= 1000:
        score += 0.35
        reasons.append("High-dollar transaction amount")

    if transaction.amount >= 5000:
        score += 0.25
        reasons.append("Very large transaction amount")

    if category in high_risk_categories:
        score += 0.20
        reasons.append(f"High-risk merchant category: {transaction.merchant_category}")

    if txn_type in high_risk_types:
        score += 0.20
        reasons.append(f"High-risk transaction type: {transaction.transaction_type}")

    if location not in trusted_locations:
        score += 0.15
        reasons.append(f"Unrecognized transaction location: {transaction.location}")

    score = min(round(score, 2), 0.99)
    return score, reasons


def get_risk_band(score: float) -> str:
    if score >= 0.70:
        return "high"
    if score >= 0.40:
        return "medium"
    return "low"


def get_recommended_action(score: float) -> str:
    if score >= 0.70:
        return "Flag for manual review"
    if score >= 0.40:
        return "Monitor transaction"
    return "Approve transaction"