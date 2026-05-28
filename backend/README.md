# Backend Setup

## 1. Create a virtual environment (Windows PowerShell)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 2. Install dependencies

```powershell
pip install -r requirements.txt
```

## 3. Run the FastAPI server

```powershell
uvicorn app.main:app --reload
```

## 4. Run tests

```powershell
pytest
```

## 5. Available endpoints

- `GET /`
- `GET /health`
- `GET /models`
- `POST /analyze`
- `POST /compare`

## 6. Sample request for `/analyze`

```json
{
  "text": "Hello world. नमस्ते दुनिया. こんにちは世界。",
  "model_ids": ["gpt-4o-mini", "gpt-4o", "bert-base-multilingual-cased"],
  "baseline_model_id": "gpt-4o-mini"
}
```

## 7. Sample request for `/compare`

`/compare` analyzes multiple text samples in one request using the same model set and baseline.

```json
{
  "texts": [
    "Hello world.",
    "नमस्ते दुनिया।"
  ],
  "model_ids": ["gpt-4o-mini", "gpt-4o"],
  "baseline_model_id": "gpt-4o-mini"
}
```

## Current MVP Features

- `/analyze` supports token count
- `/analyze` supports fertility
- `/analyze` supports cost estimate
- `/analyze` supports fairness score
- `/analyze` supports estimated latency multiplier
- Tokenizer caching is implemented
- No database/frontend yet
