from sqlalchemy import func
from sqlalchemy.orm import Session
from app import models


SORTABLE_FIELDS = {
    "created_at": models.Transaction.created_at,
    "amount": models.Transaction.amount,
    "fraud_score": models.Transaction.fraud_score,
    "ml_fraud_score": models.Transaction.ml_fraud_score,
    "merchant": models.Transaction.merchant,
}


def create_transaction(db: Session, transaction_data: dict):
    db_transaction = models.Transaction(**transaction_data)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_transactions(
    db: Session,
    status: str | None = None,
    account_id: str | None = None,
    merchant_category: str | None = None,
    min_amount: float | None = None,
    max_amount: float | None = None,
    limit: int = 10,
    offset: int = 0,
    sort_by: str = "created_at",
    sort_order: str = "desc",
):
    query = db.query(models.Transaction)

    if status:
        query = query.filter(models.Transaction.status == status)

    if account_id:
        query = query.filter(models.Transaction.account_id == account_id)

    if merchant_category:
        query = query.filter(models.Transaction.merchant_category == merchant_category)

    if min_amount is not None:
        query = query.filter(models.Transaction.amount >= min_amount)

    if max_amount is not None:
        query = query.filter(models.Transaction.amount <= max_amount)

    total_count = query.count()

    sort_column = SORTABLE_FIELDS.get(sort_by, models.Transaction.created_at)
    if sort_order.lower() == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    transactions = query.offset(offset).limit(limit).all()

    return {
        "total_count": total_count,
        "limit": limit,
        "offset": offset,
        "transactions": transactions,
    }


def get_transaction_by_transaction_id(db: Session, transaction_id: str):
    return (
        db.query(models.Transaction)
        .filter(models.Transaction.transaction_id == transaction_id)
        .first()
    )


def get_transaction_summary(db: Session):
    total_transactions = db.query(func.count(models.Transaction.id)).scalar() or 0
    total_amount = db.query(func.sum(models.Transaction.amount)).scalar() or 0
    avg_fraud_score = db.query(func.avg(models.Transaction.fraud_score)).scalar() or 0
    avg_ml_fraud_score = db.query(func.avg(models.Transaction.ml_fraud_score)).scalar() or 0

    return {
        "total_transactions": int(total_transactions),
        "total_amount": round(float(total_amount), 2),
        "average_fraud_score": round(float(avg_fraud_score), 2),
        "average_ml_fraud_score": round(float(avg_ml_fraud_score), 2),
    }


def get_high_risk_transactions(
    db: Session,
    threshold: float = 0.70,
    limit: int = 10,
    offset: int = 0,
    sort_by: str = "fraud_score",
    sort_order: str = "desc",
):
    query = db.query(models.Transaction).filter(models.Transaction.fraud_score >= threshold)

    total_count = query.count()

    sort_column = SORTABLE_FIELDS.get(sort_by, models.Transaction.fraud_score)
    if sort_order.lower() == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    transactions = query.offset(offset).limit(limit).all()

    return {
        "total_count": total_count,
        "limit": limit,
        "offset": offset,
        "transactions": transactions,
    }


def get_daily_summary(db: Session):
    rows = (
        db.query(
            func.date(models.Transaction.created_at).label("transaction_date"),
            func.count(models.Transaction.id).label("total_transactions"),
            func.sum(models.Transaction.amount).label("total_amount"),
            func.avg(models.Transaction.fraud_score).label("average_fraud_score"),
            func.avg(models.Transaction.ml_fraud_score).label("average_ml_fraud_score"),
        )
        .group_by(func.date(models.Transaction.created_at))
        .order_by(func.date(models.Transaction.created_at).desc())
        .all()
    )

    return [
        {
            "transaction_date": str(row.transaction_date),
            "total_transactions": int(row.total_transactions),
            "total_amount": round(float(row.total_amount or 0), 2),
            "average_fraud_score": round(float(row.average_fraud_score or 0), 2),
            "average_ml_fraud_score": round(float(row.average_ml_fraud_score or 0), 2),
        }
        for row in rows
    ]