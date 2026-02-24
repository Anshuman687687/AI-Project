"""
FastAPI backend for Loan Approval demo

Endpoints:
- GET  /            -> serves index.html
- GET  /api/models  -> returns available models and demo accuracies
- POST /api/predict -> accepts applicant data and returns Approved/Rejected

This keeps the same demo scoring logic as the frontend so behaviour matches.
"""

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(title="Loan Approval API")

# Allow local dev from any origin (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (index.html and assets) from the repo root
app.mount("/static", StaticFiles(directory="."), name="static")


class PredictRequest(BaseModel):
    model: str
    income_annum: Optional[float] = 0
    loan_amount: Optional[float] = 0
    loan_term: Optional[float] = 0
    cibil_score: Optional[float] = 0
    residential_assets_value: Optional[float] = 0
    commercial_assets_value: Optional[float] = 0
    luxury_assets_value: Optional[float] = 0
    bank_asset_value: Optional[float] = 0
    self_employed: Optional[str] = "No"


@app.get("/")
def read_index():
    return FileResponse("index.html")


@app.get("/api/models")
def get_models():
    # Demo accuracies matching frontend defaults
    return {
        "models": {
            "logistic": {"name": "Logistic Regression", "accuracy": 0.86},
            "lgbm": {"name": "LightGBM (LGBM)", "accuracy": 0.91},
            "decision_tree": {"name": "Decision Tree", "accuracy": 0.84},
            "xgboost": {"name": "XGBoost", "accuracy": 0.93},
        }
    }


@app.post("/api/predict")
def predict(req: PredictRequest):
    # Implement same demo scoring logic as frontend so results align
    income = float(req.income_annum or 0)
    loan = float(req.loan_amount or 0)
    cibil = float(req.cibil_score or 0)

    res = float(req.residential_assets_value or 0)
    com = float(req.commercial_assets_value or 0)
    lux = float(req.luxury_assets_value or 0)
    bank = float(req.bank_asset_value or 0)

    selfEmp = (req.self_employed or "No")

    score = 0.0

    # CIBIL
    if cibil >= 750:
        score += 3
    elif cibil >= 650:
        score += 2
    elif cibil >= 550:
        score += 1

    # income/loan ratio
    if loan > 0:
        r = income / loan
        if r >= 0.6:
            score += 3
        elif r >= 0.4:
            score += 2
        elif r >= 0.25:
            score += 1

    # assets
    assets = res + com + lux + bank
    if assets >= loan:
        score += 2
    elif assets >= loan * 0.5:
        score += 1

    # small penalty
    if selfEmp == "Yes":
        score -= 0.5

    # model thresholds (demo)
    threshold = 5.0
    if req.model == "decision_tree":
        threshold = 5.5
    if req.model == "lgbm":
        threshold = 4.8
    if req.model == "xgboost":
        threshold = 4.6

    approved = score >= threshold

    return JSONResponse({
        "approved": bool(approved),
        "message": "Approved ✅" if approved else "Rejected ❌",
        "score": score,
        "threshold": threshold,
    })


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)