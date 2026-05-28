from fastapi import APIRouter, HTTPException

from app.core.config import DEFAULT_BASELINE_MODEL
from app.core.model_registry import get_model
from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse, ModelAnalysis
from app.services.metrics_service import (
    calculate_attention_cost_multiplier,
    calculate_fairness_score,
    calculate_fertility,
    calculate_token_multiplier,
    count_characters_no_spaces,
    count_words,
)
from app.services.pricing_service import calculate_input_cost
from app.services.tokenizer_service import count_tokens

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_text(payload: AnalyzeRequest) -> AnalyzeResponse:
    text = payload.text

    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Text must not be empty or whitespace.")

    if not payload.model_ids:
        raise HTTPException(status_code=400, detail="model_ids must contain at least one model id.")

    if len(set(payload.model_ids)) != len(payload.model_ids):
        raise HTTPException(status_code=400, detail="model_ids must not contain duplicates.")

    baseline_model_id = payload.baseline_model_id or DEFAULT_BASELINE_MODEL

    try:
        get_model(baseline_model_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown baseline_model_id '{baseline_model_id}'.",
        ) from exc

    selected_models: dict[str, dict[str, object]] = {}
    for model_id in payload.model_ids:
        try:
            selected_models[model_id] = get_model(model_id)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=f"Unknown model_id '{model_id}'.") from exc

    try:
        baseline_token_count = count_tokens(text, baseline_model_id)
    except (RuntimeError, ValueError) as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    analyses: list[ModelAnalysis] = []
    word_count = count_words(text)
    character_count_no_spaces = count_characters_no_spaces(text)

    for model_id in payload.model_ids:
        model_info = selected_models[model_id]

        try:
            token_count = count_tokens(text, model_id)
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

        token_multiplier = calculate_token_multiplier(token_count, baseline_token_count)
        estimated_attention_cost_multiplier = calculate_attention_cost_multiplier(token_multiplier)

        analyses.append(
            ModelAnalysis(
                model_id=str(model_info["id"]),
                display_name=str(model_info["display_name"]),
                provider=str(model_info["provider"]),
                token_count=token_count,
                word_count=word_count,
                character_count_no_spaces=character_count_no_spaces,
                fertility=calculate_fertility(token_count, word_count),
                token_multiplier=token_multiplier,
                estimated_attention_cost_multiplier=estimated_attention_cost_multiplier,
                estimated_latency_multiplier=token_multiplier,
                input_cost_estimate_usd=calculate_input_cost(
                    token_count,
                    float(model_info["input_price_per_million_tokens"]),
                ),
                fairness_score=calculate_fairness_score(token_multiplier),
            )
        )

    return AnalyzeResponse(
        baseline_model_id=baseline_model_id,
        text_preview=text[:120],
        analyses=analyses,
    )
