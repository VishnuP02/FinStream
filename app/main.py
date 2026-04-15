import logging

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app import models, schemas, crud
from app.seed_data import sample_transactions
from app.risk import calculate_fraud_score, get_risk_band, get_recommended_action

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FinStream API", version="3.0.0")


@app.get("/")
def root():
    return {"message": "Welcome to FinStream API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/transactions", response_model=schemas.TransactionResponse)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
):
    existing = crud.get_transaction_by_transaction_id(db, transaction.transaction_id)
    if existing:
        raise HTTPException(status_code=400, detail="Transaction ID already exists")

    fraud_score, reasons = calculate_fraud_score(transaction)

    # Lazy import to avoid startup hangs from ML dependencies
    from app.ml_model import predict_ml_fraud_score
    ml_fraud_score = predict_ml_fraud_score(transaction)

    combined_score = round((fraud_score + ml_fraud_score) / 2, 2)
    status = "flagged" if combined_score >= 0.70 else "approved"

    transaction_data = transaction.model_dump()
    transaction_data["fraud_score"] = fraud_score
    transaction_data["ml_fraud_score"] = ml_fraud_score
    transaction_data["status"] = status

    db_transaction = crud.create_transaction(db, transaction_data)

    logger.info(
        "Created transaction=%s status=%s fraud_score=%.2f ml_fraud_score=%.2f reasons=%s",
        db_transaction.transaction_id,
        status,
        fraud_score,
        ml_fraud_score,
        reasons,
    )

    return db_transaction


@app.get("/transactions", response_model=schemas.PaginatedTransactionResponse)
def get_transactions(
    status: str | None = Query(default=None),
    account_id: str | None = Query(default=None),
    merchant_category: str | None = Query(default=None),
    min_amount: float | None = Query(default=None),
    max_amount: float | None = Query(default=None),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    sort_by: str = Query(default="created_at"),
    sort_order: str = Query(default="desc"),
    db: Session = Depends(get_db),
):
    logger.info(
        "Fetching transactions status=%s account_id=%s category=%s min_amount=%s max_amount=%s limit=%s offset=%s sort_by=%s sort_order=%s",
        status,
        account_id,
        merchant_category,
        min_amount,
        max_amount,
        limit,
        offset,
        sort_by,
        sort_order,
    )
    return crud.get_transactions(
        db=db,
        status=status,
        account_id=account_id,
        merchant_category=merchant_category,
        min_amount=min_amount,
        max_amount=max_amount,
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@app.get("/transactions/{transaction_id}", response_model=schemas.TransactionResponse)
def get_transaction(transaction_id: str, db: Session = Depends(get_db)):
    transaction = crud.get_transaction_by_transaction_id(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@app.get("/summary", response_model=schemas.SummaryResponse)
def get_summary(db: Session = Depends(get_db)):
    return crud.get_transaction_summary(db)


@app.get("/fraudulent-transactions", response_model=schemas.PaginatedTransactionResponse)
def get_fraudulent_transactions(
    threshold: float = Query(default=0.70, ge=0.0, le=1.0),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    sort_by: str = Query(default="fraud_score"),
    sort_order: str = Query(default="desc"),
    db: Session = Depends(get_db),
):
    logger.info(
        "Fetching fraudulent transactions threshold=%s limit=%s offset=%s sort_by=%s sort_order=%s",
        threshold,
        limit,
        offset,
        sort_by,
        sort_order,
    )
    return crud.get_high_risk_transactions(
        db=db,
        threshold=threshold,
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@app.get("/risk-assessment/{transaction_id}", response_model=schemas.RiskAssessmentResponse)
def get_risk_assessment(transaction_id: str, db: Session = Depends(get_db)):
    transaction = crud.get_transaction_by_transaction_id(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    rule_score = float(transaction.fraud_score)
    ml_score = float(transaction.ml_fraud_score)
    combined_score = round((rule_score + ml_score) / 2, 2)

    risk_band = get_risk_band(combined_score)
    recommended_action = get_recommended_action(combined_score)

    _, reasons = calculate_fraud_score(transaction)
    if not reasons:
        reasons = ["No major risk indicators detected"]

    return {
        "transaction_id": transaction.transaction_id,
        "fraud_score": rule_score,
        "ml_fraud_score": ml_score,
        "combined_risk_score": combined_score,
        "risk_band": risk_band,
        "reasons": reasons,
        "recommended_action": recommended_action,
    }


@app.get("/daily-summary", response_model=list[schemas.DailySummaryItem])
def daily_summary(db: Session = Depends(get_db)):
    return crud.get_daily_summary(db)


@app.post("/seed")
def seed_database(db: Session = Depends(get_db)):
    inserted = 0

    for txn in sample_transactions:
        existing = crud.get_transaction_by_transaction_id(db, txn["transaction_id"])
        if not existing:
            transaction_obj = schemas.TransactionCreate(**txn)
            rule_score, reasons = calculate_fraud_score(transaction_obj)

            # Lazy import to avoid startup hangs from ML dependencies
            from app.ml_model import predict_ml_fraud_score
            ml_score = predict_ml_fraud_score(transaction_obj)

            combined_score = round((rule_score + ml_score) / 2, 2)
            status = "flagged" if combined_score >= 0.70 else "approved"

            transaction_data = transaction_obj.model_dump()
            transaction_data["fraud_score"] = rule_score
            transaction_data["ml_fraud_score"] = ml_score
            transaction_data["status"] = status

            crud.create_transaction(db, transaction_data)
            inserted += 1

            logger.info(
                "Seeded transaction=%s status=%s fraud_score=%.2f ml_fraud_score=%.2f reasons=%s",
                transaction_obj.transaction_id,
                status,
                rule_score,
                ml_score,
                reasons,
            )

    return {"message": f"Inserted {inserted} sample transactions"}