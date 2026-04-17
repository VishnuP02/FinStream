# FinStream API

FinStream is a fraud detection backend built with FastAPI, PostgreSQL, SQLAlchemy, and a lightweight Logistic Regression model. It analyzes financial transactions using both rule-based logic and machine learning, then exposes results through REST APIs for analytics and investigation.

---

## 🚀 Features

- FastAPI backend with interactive Swagger docs  
- PostgreSQL database with SQLAlchemy ORM  
- Rule-based fraud scoring system  
- ML-based fraud prediction using Logistic Regression  
- Hybrid risk scoring (rules + ML)  
- Explainable risk assessment with reasons and recommended actions  
- Filtering, sorting, pagination, and summaries  
- Seed endpoint for realistic transaction simulation  

---

## 🛠 Tech Stack

- Python  
- FastAPI  
- PostgreSQL  
- SQLAlchemy  
- scikit-learn  
- NumPy  
- Uvicorn  

---

## 📁 Project Structure

```
FinStream/
├── app/
│   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── ml_model.py
│   ├── models.py
│   ├── risk.py
│   ├── schemas.py
│   ├── seed_data.py
├── .env.example
├── .gitignore
├── requirements.txt
├── run.py
```

---

## 🌐 Live Demo

- API Base URL: https://finstream-m42n.onrender.com  
- Swagger Docs: https://finstream-m42n.onrender.com/docs  

---

## 📡 API Endpoints

### Core

- GET / → Welcome message  
- GET /health → Health check  

### Transactions

- POST /transactions → Create transaction  
- GET /transactions → List transactions  
- GET /transactions/{id} → Get transaction  

### Analytics

- GET /fraudulent-transactions?threshold=0.7  
- GET /daily-summary  
- GET /risk-assessment/{transaction_id}  

### Utilities

- POST /seed → Load sample transactions  

---

## 🧪 Example API Calls

```bash
curl https://finstream-m42n.onrender.com/health
curl -X POST https://finstream-m42n.onrender.com/seed
curl "https://finstream-m42n.onrender.com/fraudulent-transactions?threshold=0.7"
curl https://finstream-m42n.onrender.com/daily-summary
curl https://finstream-m42n.onrender.com/risk-assessment/TXN1006
```

---

## 🧠 How It Works

### Rule-Based Detection

- Large transaction amounts  
- High-risk categories (wire, transfer, crypto, etc.)  
- Unrecognized or risky locations  

### Machine Learning Model

Uses Logistic Regression with:
- Transaction amount  
- Merchant category  
- Transaction type  
- Location risk  

### Hybrid Scoring

Combines rule-based detection with ML probability into a final risk score and risk band.

---

## 📊 Example Response

```json
{
  "transaction_id": "TXN1006",
  "fraud_score": 0.99,
  "ml_fraud_score": 1.0,
  "risk_band": "high",
  "reasons": [
    "High-dollar transaction amount",
    "Very large transaction amount",
    "High-risk merchant category",
    "High-risk transaction type",
    "Unrecognized transaction location"
  ],
  "recommended_action": "Flag for manual review"
}
```

---

## ⚙️ Local Setup

```bash
git clone <your-repo-url>
cd FinStream

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file:

```
DATABASE_URL=postgresql://username:password@localhost:5432/finstream
```

Run the server:

```bash
python3 run.py
```

Open docs:

```
http://127.0.0.1:8000/docs
```

---

## 🚀 Deployment

Recommended platforms:
- Render
- Railway
