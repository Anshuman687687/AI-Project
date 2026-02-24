# Loan Approval Demo (FastAPI + Frontend)

This project serves the frontend `index.html` and provides a small FastAPI backend that exposes demo model metadata and a prediction endpoint.

Prerequisites
- Python 3.8+

Quick start (Windows PowerShell)

1. Open PowerShell and change to the project folder:

```powershell
cd 'C:\Users\hp\Desktop\anshu'
```

2. (Optional but recommended) create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Start the FastAPI server:

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

5. Open the app in your browser:

- http://127.0.0.1:8000/

API endpoints
- `GET /api/models` — returns available demo models and accuracies
- `POST /api/predict` — accepts JSON payload (see examples) and returns prediction JSON

Example payload for `/api/predict` (fields match the frontend form):

```json
{
  "model": "logistic",
  "income_annum": 9600000,
  "loan_amount": 29900000,
  "loan_term": 12,
  "cibil_score": 778,
  "residential_assets_value": 2400000,
  "commercial_assets_value": 17600000,
  "luxury_assets_value": 22700000,
  "bank_asset_value": 0,
  "self_employed": "No"
}
```

Curl / PowerShell test examples

PowerShell (recommended on Windows):

```powershell
#$body can be built as a PowerShell hashtable and converted to JSON
$body = @{
  model = 'logistic'
  income_annum = 9600000
  loan_amount = 29900000
  loan_term = 12
  cibil_score = 778
  residential_assets_value = 2400000
  commercial_assets_value = 17600000
  luxury_assets_value = 22700000
  bank_asset_value = 0
  self_employed = 'No'
} | ConvertTo-Json

Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/predict' -Method POST -Body $body -ContentType 'application/json'
```

If you prefer `curl` (bash / WSL / Git Bash), use:

```bash
curl -X POST 'http://127.0.0.1:8000/api/predict' \
  -H 'Content-Type: application/json' \
  -d '{"model":"logistic","income_annum":9600000,"loan_amount":29900000,"loan_term":12,"cibil_score":778,"residential_assets_value":2400000,"commercial_assets_value":17600000,"luxury_assets_value":22700000,"bank_asset_value":0,"self_employed":"No"}'
```

Example: quickly get model metadata

PowerShell:
```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/models' -Method GET
```

curl:
```bash
curl http://127.0.0.1:8000/api/models
```

Troubleshooting
- If your request fails, ensure the uvicorn server is running and listening on port `8000`.
- On Windows, `curl` in PowerShell can behave differently—use `Invoke-RestMethod` or run `curl` from WSL/Git Bash if you see parsing issues.
- If port conflicts occur, change `--port` to an available port and update the URLs accordingly.

Files of interest
- `main.py` — FastAPI application
- `index.html` — frontend UI (calls `/api/predict`)
- `requirements.txt` — Python dependencies

If you'd like, I can also add a small PowerShell script to run the test request for you.
