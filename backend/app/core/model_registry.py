from __future__ import annotations

from typing import Any

MODEL_REGISTRY: dict[str, dict[str, Any]] = {
    "gpt-4o-mini": {
        "id": "gpt-4o-mini",
        "display_name": "GPT-4o mini",
        "provider": "OpenAI",
        "tokenizer_type": "tiktoken",
        "tokenizer_name": "o200k_base",
        "input_price_per_million_tokens": 0.15,
        "notes": "Efficient OpenAI model using o200k tokenizer family.",
    },
    "gpt-4o": {
        "id": "gpt-4o",
        "display_name": "GPT-4o",
        "provider": "OpenAI",
        "tokenizer_type": "tiktoken",
        "tokenizer_name": "o200k_base",
        "input_price_per_million_tokens": 2.50,
        "notes": "General-purpose OpenAI model using o200k tokenizer family.",
    },
    "bert-base-multilingual-cased": {
        "id": "bert-base-multilingual-cased",
        "display_name": "BERT Base Multilingual Cased",
        "provider": "Hugging Face",
        "tokenizer_type": "huggingface",
        "tokenizer_name": "bert-base-multilingual-cased",
        "input_price_per_million_tokens": 0.00,
        "notes": "Open multilingual tokenizer/model checkpoint.",
    },
    "xlm-roberta-base": {
        "id": "xlm-roberta-base",
        "display_name": "XLM-RoBERTa Base",
        "provider": "Hugging Face",
        "tokenizer_type": "huggingface",
        "tokenizer_name": "xlm-roberta-base",
        "input_price_per_million_tokens": 0.00,
        "notes": "Open multilingual tokenizer/model checkpoint.",
    },
}


def list_models() -> list[dict[str, Any]]:
    return [MODEL_REGISTRY[model_id].copy() for model_id in MODEL_REGISTRY]


def get_model(model_id: str) -> dict[str, Any]:
    model = MODEL_REGISTRY.get(model_id)
    if model is None:
        raise ValueError(f"Unknown model_id '{model_id}'. Available models: {', '.join(MODEL_REGISTRY.keys())}")
    return model.copy()
