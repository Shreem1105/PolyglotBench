from app.core.model_registry import get_model
from app.schemas.analyze import ModelAnalysis
from app.services.language_service import detect_language
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


def analyze_text_against_models(
    text: str,
    model_ids: list[str],
    baseline_model_id: str,
) -> list[ModelAnalysis]:
    try:
        get_model(baseline_model_id)
    except ValueError as exc:
        raise ValueError(f"Unknown baseline_model_id '{baseline_model_id}'.") from exc

    selected_models: dict[str, dict[str, object]] = {}
    for model_id in model_ids:
        try:
            selected_models[model_id] = get_model(model_id)
        except ValueError as exc:
            raise ValueError(f"Unknown model_id '{model_id}'.") from exc

    baseline_token_count = count_tokens(text, baseline_model_id)

    analyses: list[ModelAnalysis] = []
    language_detected = detect_language(text)
    word_count = count_words(text)
    character_count_no_spaces = count_characters_no_spaces(text)

    for model_id in model_ids:
        model_info = selected_models[model_id]
        token_count = count_tokens(text, model_id)

        token_multiplier = calculate_token_multiplier(token_count, baseline_token_count)
        estimated_attention_cost_multiplier = calculate_attention_cost_multiplier(
            token_multiplier
        )

        analyses.append(
            ModelAnalysis(
                model_id=str(model_info["id"]),
                display_name=str(model_info["display_name"]),
                provider=str(model_info["provider"]),
                language_detected=language_detected,
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

    return analyses
