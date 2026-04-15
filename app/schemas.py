from datetime import datetime
from pydantic import BaseModel, Field


class TransactionBase(BaseModel):
    transaction_id: str = Field(..., examples=["TXN2001"])
    account_id: str = Field(..., examples=["ACC7001"])
    merchant: str = Field(..., examples=["Amazon"])
    merchant_category: str = Field(..., examples=["Retail"])
    amount: float = Field(..., examples=[149.99])
    transaction_type: str = Field(..., examples=["debit_card"])
    location: str = Field(..., examples=["Philadelphia, PA"])


class TransactionCreate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    id: int
    status: str
    fraud_score: float
    ml_fraud_score: float
    created_at: datetime

    class Config:
        from_attributes = True


class SummaryResponse(BaseModel):
    total_transactions: int
    total_amount: float
    average_fraud_score: float
    average_ml_fraud_score: float


class DailySummaryItem(BaseModel):
    transaction_date: str
    total_transactions: int
    total_amount: float
    average_fraud_score: float
    average_ml_fraud_score: float


class RiskAssessmentResponse(BaseModel):
    transaction_id: str
    fraud_score: float
    ml_fraud_score: float
    combined_risk_score: float
    risk_band: str
    reasons: list[str]
    recommended_action: str


class PaginatedTransactionResponse(BaseModel):
    total_count: int
    limit: int
    offset: int
    transactions: list[TransactionResponse]