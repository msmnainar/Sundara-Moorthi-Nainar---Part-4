# D2C Churn Prediction API – FastAPI Service

## Overview
This project builds a FastAPI service that provides churn-risk predictions for customers. It loads a trained model and exposes endpoints for individual and batch predictions.

---

## Objective
- Provide real-time churn prediction API
- Integrate with CRM systems
- Support batch scoring

---

## Project Structure

app/
  main.py
model.pkl
test_api.py
requirements.txt
monitoring_plan.md

---

## Setup Instructions

1. Install dependencies:
pip install -r requirements.txt

2. Run API:
uvicorn app.main:app --reload

---

## API Endpoints

### 1. Health Check
GET /health

Response:
{
  "status": "ok"
}

---

### 2. Predict (Single Customer)
POST /predict

Sample Request:
{
  "recency": 60,
  "frequency": 3,
  "monetary": 2500,
  "ticket_count": 2,
  "avg_sentiment": 0.2
}

Response:
{
  "churn_probability": 0.72,
  "predicted_class": 1,
  "risk_level": "high",
  "risk_explanation": "High inactivity and negative support signals indicate churn risk"
}

---

### 3. Batch Predict
POST /batch_predict

Request:
[
  {...},
  {...}
]

Response:
[
  {...},
  {...}
]

---

## Running Tests

python test_api.py

---

## Model Notes
- Model: Random Forest
- Features: RFM + support metrics
- No leakage (snapshot-based filtering applied)

---

## Conclusion
This API enables real-time churn prediction and supports business retention strategies.
