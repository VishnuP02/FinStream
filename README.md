# FinStream API

FinStream is a fraud detection backend built with FastAPI, PostgreSQL, SQLAlchemy, and a lightweight Logistic Regression model. It scores transactions using both rule-based logic and machine learning, and exposes results through REST APIs for analytics and investigation.

---

## 🚀 Features

* FastAPI backend with interactive Swagger docs
* PostgreSQL database with SQLAlchemy ORM
* Rule-based fraud scoring system
* ML fraud prediction using Logistic Regression
* Risk assessment with explanations + recommendations
* Filtering, sorting, pagination, and summaries
* Seed endpoint for realistic transaction simulation

---

## 🛠️ Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* scikit-learn
* NumPy
* Uvicorn

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
│   └── seed_data.py
├── .env.example
├── .gitignore
├── requirements.txt
└── run.py
```

---

## 🌐 API Endpoints

### Core

* `GET /` → Welcome message
* `GET /health` → Health check

### Transactions

* `POST /transactions` → Create transaction
* `GET /transactions` → List transactions
* `GET /transactions/{id}` → Get one transaction

### Analytics

* `GET /fraudulent-transactions?threshold=0.7`
* `GET /daily-summary`
* `GET /risk-assessment/{transaction_id}`

### Utilities

* `POST /seed` → Load sample transactions

---

## ⚙️ Local Setup

### 1. Clone repo

```
git clone <your-repo-url>
cd FinStream
```

### 2. Create virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Create `.env`

```
DATABASE_URL=postgresql://username:password@127.0.0.1:5432/finstream
```

⚠️ If your password has `@`, replace with `%40`

---

### 5. Run the server

```
python3 run.py
```

---

### 6. Open API Docs

```
http://127.0.0.1:8000/docs
```

---

## 🧪 Example API Calls

```
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/seed
curl "http://127.0.0.1:8000/fraudulent-transactions?threshold=0.7"
curl http://127.0.0.1:8000/daily-summary
curl http://127.0.0.1:8000/risk-assessment/TXN1006
```

---

## 🧠 How It Works

* Rule-based scoring flags high-risk patterns:

  * Large transaction amounts
  * Suspicious categories (crypto, wire, etc.)
  * Unrecognized locations

* ML model predicts fraud probability using:

  * Amount
  * Category
  * Transaction type
  * Location risk

* Final output combines both into:

  * `fraud_score`
  * `ml_fraud_score`
  * `risk_band`
  * `recommended_action`

---

## 🔐 Environment Setup

Create `.env.example`:

```
DATABASE_URL=postgresql://username:password@localhost:5432/finstream
```

---

## 📊 Resume Description

Built a fraud detection API using FastAPI, PostgreSQL, SQLAlchemy, and Logistic Regression to score transactions, flag high-risk activity, and provide real-time analytics through REST endpoints.

---

## 🚀 Deployment

Recommended platforms:

* Render
* Railway

Start command:

```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## 🎯 Future Improvements

* Frontend dashboard (React)
* Real-time streaming detection (Kafka)
* Model retraining pipeline
* Authentication system

---
