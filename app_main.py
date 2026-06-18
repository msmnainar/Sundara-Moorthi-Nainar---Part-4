from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
import numpy as np
import joblib
import os

from google.colab import files
files.upload()

# =====================================================
# INIT APP
# =====================================================
app = FastAPI(title="D2C Churn Prediction API")

# =====================================================
# GLOBAL MODEL VARIABLE
# =====================================================
model = None
MODEL_PATH = "model.pkl"

# =====================================================
# LOAD MODEL (IF EXISTS)
# =====================================================
def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("✅ Model loaded successfully")
    else:
        print("⚠️ model.pkl not found - please upload model")

load_model()

# =====================================================
# INPUT SCHEMA
# =====================================================
class Customer(BaseModel):
    recency: float = Field(gt=0)
    frequency: float = Field(ge=0)
    monetary: float = Field(ge=0)
    ticket_count: float = Field(ge=0)
    avg_sentiment: float = Field(ge=-1, le=1)

# =====================================================
# HELPER FUNCTIONS
# =====================================================
def ensure_model():
    if model is None:
        raise HTTPException(
            status_code=500,
            detail="Model not loaded. Upload model.pkl using /upload_model endpoint"
        )

def get_risk_level(prob):
    if prob >= 0.7:
        return "high"
    elif prob >= 0.4:
        return "medium"
    else:
        return "low"

def get_explanation(data: Customer):
    reasons = []

    if data.recency > 60:
        reasons.append("high inactivity")

    if data.ticket_count > 3:
        reasons.append("frequent issues")

    if data.avg_sentiment < 0:
        reasons.append("negative sentiment")

    if data.frequency < 2:
        reasons.append("low purchase frequency")

    if not reasons:
        return "stable customer behavior"

    return ", ".join(reasons)

# =====================================================
# ENDPOINTS
# =====================================================

# ✅ Health Check
@app.get("/health")
def health():
    return {"status": "ok"}


# ✅ Upload Model (NEW ✅ VERY IMPORTANT)
@app.post("/upload_model")
async def upload_model(file: UploadFile = File(...)):
    global model

    # Save uploaded file
    with open(MODEL_PATH, "wb") as f:
        f.write(await file.read())

    # Load model
    model = joblib.load(MODEL_PATH)

    return {"message": "✅ Model uploaded and loaded successfully"}


# ✅ Single Prediction
@app.post("/predict")
def predict(customer: Customer):
    ensure_model()

    features = np.array([[
        customer.recency,
        customer.frequency,
        customer.monetary,
        customer.ticket_count,
        customer.avg_sentiment
    ]])

    prob = float(model.predict_proba(features)[0][1])
    pred = int(prob >= 0.5)

    return {
        "churn_probability": round(prob, 2),
        "predicted_class": pred,
        "risk_level": get_risk_level(prob),
        "risk_explanation": get_explanation(customer)
    }


# ✅ Batch Prediction
@app.post("/batch_predict")
def batch_predict(customers: list[Customer]):
    ensure_model()

    results = []

    for c in customers:
        features = np.array([[
            c.recency,
            c.frequency,
            c.monetary,
            c.ticket_count,
            c.avg_sentiment
        ]])

        prob = float(model.predict_proba(features)[0][1])
        pred = int(prob >= 0.5)

        results.append({
            "churn_probability": round(prob, 2),
            "predicted_class": pred,
            "risk_level": get_risk_level(prob)
        })

    return results