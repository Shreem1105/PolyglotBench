import csv
import io

from app.schemas.analyze import ModelAnalysis


def analyses_to_csv(analyses: list[ModelAnalysis]) -> str:
    output = io.StringIO()
    fieldnames = [
        "model_id",
        "display_name",
        "provider",
        "token_count",
        "word_count",
        "character_count_no_spaces",
        "fertility",
        "token_multiplier",
        "estimated_attention_cost_multiplier",
        "estimated_latency_multiplier",
        "input_cost_estimate_usd",
        "fairness_score",
    ]

    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for analysis in analyses:
        writer.writerow(
            {
                "model_id": analysis.model_id,
                "display_name": analysis.display_name,
                "provider": analysis.provider,
                "token_count": analysis.token_count,
                "word_count": analysis.word_count,
                "character_count_no_spaces": analysis.character_count_no_spaces,
                "fertility": analysis.fertility,
                "token_multiplier": analysis.token_multiplier,
                "estimated_attention_cost_multiplier": analysis.estimated_attention_cost_multiplier,
                "estimated_latency_multiplier": analysis.estimated_latency_multiplier,
                "input_cost_estimate_usd": analysis.input_cost_estimate_usd,
                "fairness_score": analysis.fairness_score,
            }
        )

    return output.getvalue()
