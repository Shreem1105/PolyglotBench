# API Examples

Base URL (local): `http://localhost:8000`

## GET /models
### Request
```bash
curl "http://localhost:8000/models"
```

### Response (abbreviated)
```json
{
  "models": [
    {
      "id": "gpt-4o-mini",
      "display_name": "GPT-4o mini",
      "provider": "OpenAI",
      "tokenizer_type": "tiktoken",
      "tokenizer_name": "o200k_base",
      "input_price_per_million_tokens": 0.15,
      "notes": "Baseline-friendly low-cost model."
    }
  ]
}
```

## POST /analyze
### Request
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Artificial intelligence is changing how people build software.",
    "model_ids": ["gpt-4o-mini", "gpt-4o"],
    "baseline_model_id": "gpt-4o-mini"
  }'
```

### Response (abbreviated)
```json
{
  "baseline_model_id": "gpt-4o-mini",
  "text_preview": "Artificial intelligence is changing how people build software.",
  "analyses": [
    {
      "model_id": "gpt-4o-mini",
      "display_name": "GPT-4o mini",
      "provider": "OpenAI",
      "language_detected": "en",
      "token_count": 11,
      "word_count": 8,
      "fertility": 1.375,
      "token_multiplier": 1.0,
      "estimated_attention_cost_multiplier": 1.0,
      "estimated_latency_multiplier": 1.0,
      "input_cost_estimate_usd": 0.00000165,
      "fairness_score": 100.0
    }
  ]
}
```

## POST /compare
### Request
```bash
curl -X POST "http://localhost:8000/compare" \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "Artificial intelligence is changing software engineering.",
      "कृत्रिम बुद्धिमत्ता सॉफ्टवेयर विकास को बदल रही है।"
    ],
    "model_ids": ["gpt-4o-mini", "xlm-roberta-base"],
    "baseline_model_id": "gpt-4o-mini"
  }'
```

### Response (abbreviated)
```json
{
  "total_texts": 2,
  "model_ids": ["gpt-4o-mini", "xlm-roberta-base"],
  "baseline_model_id": "gpt-4o-mini",
  "results": [
    {
      "text_index": 0,
      "text_preview": "Artificial intelligence is changing software engineering.",
      "baseline_model_id": "gpt-4o-mini",
      "analyses": [
        {
          "model_id": "gpt-4o-mini",
          "fairness_score": 100.0
        }
      ]
    }
  ]
}
```

## POST /export (JSON)
### Request
```bash
curl -X POST "http://localhost:8000/export" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "الذكاء الاصطناعي يغير طريقة بناء البرمجيات.",
    "model_ids": ["gpt-4o-mini", "gpt-4o"],
    "format": "json"
  }'
```

### Response (abbreviated)
```json
{
  "project": "PolyglotBench",
  "export_format": "json",
  "baseline_model_id": "gpt-4o-mini",
  "text_preview": "الذكاء الاصطناعي يغير طريقة بناء البرمجيات.",
  "analyses": [
    {
      "model_id": "gpt-4o-mini",
      "fairness_score": 100.0
    }
  ]
}
```

## POST /export (CSV)
### Request
```bash
curl -X POST "http://localhost:8000/export" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Artificial intelligence is changing software engineering.",
    "model_ids": ["gpt-4o-mini", "gpt-4o"],
    "format": "csv"
  }'
```

### Response Headers (abbreviated)
```text
HTTP/1.1 200 OK
content-type: text/csv; charset=utf-8
content-disposition: attachment; filename="polyglotbench_export.csv"
```

### Response Body (abbreviated)
```csv
model_id,display_name,provider,token_count,word_count,character_count_no_spaces,fertility,token_multiplier,estimated_attention_cost_multiplier,estimated_latency_multiplier,input_cost_estimate_usd,fairness_score
gpt-4o-mini,GPT-4o mini,OpenAI,11,8,55,1.3750,1.0000,1.0000,1.0000,0.00000165,100.0000
```

## GET /leaderboard
### Request
```bash
curl "http://localhost:8000/leaderboard"
```

### Response (abbreviated)
```json
{
  "languages": ["English", "Hindi", "Arabic", "Tamil", "Chinese"],
  "models": ["gpt-4o-mini", "gpt-4o", "bert-base-multilingual-cased", "xlm-roberta-base"],
  "leaderboard": [
    {
      "rank": 1,
      "model_id": "gpt-4o-mini",
      "average_fairness_score": 87.42
    }
  ]
}
```

## POST /submissions/from-analysis
### Request
```bash
curl -X POST "http://localhost:8000/submissions/from-analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Artificial intelligence is changing software engineering.",
    "model_ids": ["gpt-4o-mini", "gpt-4o"],
    "baseline_model_id": "gpt-4o-mini"
  }'
```

### Response (abbreviated)
```json
{
  "id": 14,
  "text_preview": "Artificial intelligence is changing software engineering.",
  "language_detected": "en",
  "selected_models": ["gpt-4o-mini", "gpt-4o"],
  "baseline_model_id": "gpt-4o-mini",
  "min_fairness_score": 84.6154,
  "max_token_multiplier": 1.1818,
  "created_at": "2026-05-29T12:40:04.884112"
}
```

## GET /submissions
### Request
```bash
curl "http://localhost:8000/submissions?limit=5"
```

### Response (abbreviated)
```json
{
  "submissions": [
    {
      "id": 14,
      "language_detected": "en",
      "selected_models": ["gpt-4o-mini", "gpt-4o"],
      "baseline_model_id": "gpt-4o-mini",
      "min_fairness_score": 84.6154,
      "max_token_multiplier": 1.1818,
      "created_at": "2026-05-29T12:40:04.884112"
    }
  ]
}
```
