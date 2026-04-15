# FinStream API

FinStream is a fraud detection backend built with FastAPI, PostgreSQL, SQLAlchemy, and a lightweight Logistic Regression model. It scores transactions with both rule-based logic and ML-assisted risk prediction, then exposes the results through REST endpoints for analytics and investigation.

## Features

- FastAPI backend with interactive Swagger docs
- PostgreSQL database integration with SQLAlchemy ORM
- Rule-based fraud scoring
- ML-assisted fraud scoring with Logistic Regression
- Risk assessment endpoint with reasons and recommended action
- Transaction filtering, sorting, pagination, and summaries
- Seed endpoint for loading realistic sample transactions

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- scikit-learn
- NumPy
- Uvicorn

## Project Structure

```text
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
