from app.core.config import DEFAULT_BASELINE_MODEL
from app.core.model_registry import get_model, list_models
from app.services.analysis_service import analyze_text_against_models

BENCHMARK_SAMPLES: list[tuple[str, str]] = [
    (
        "English",
        "Artificial intelligence is changing how people build software.",
    ),
    (
        "Hindi",
        "कृत्रिम बुद्धिमत्ता सॉफ्टवेयर बनाने के तरीके को बदल रही है।",
    ),
    (
        "Arabic",
        "الذكاء الاصطناعي يغير طريقة بناء البرمجيات.",
    ),
    (
        "Tamil",
        "செயற்கை நுண்ணறிவு மென்பொருள் உருவாக்கும் முறையை மாற்றுகிறது.",
    ),
    (
        "Chinese",
        "人工智能正在改变人们构建软件的方式。",
    ),
    (
        "Japanese",
        "人工知能は人々のソフトウェア開発の方法を変えています。",
    ),
    (
        "Korean",
        "인공지능은 사람들이 소프트웨어를 만드는 방식을 바꾸고 있습니다.",
    ),
    (
        "Spanish",
        "La inteligencia artificial esta cambiando como las personas crean software.",
    ),
    (
        "French",
        "L intelligence artificielle transforme la facon dont les gens creent des logiciels.",
    ),
    (
        "German",
        "Kuenstliche Intelligenz veraendert, wie Menschen Software entwickeln.",
    ),
]


def generate_fairness_leaderboard(
    baseline_model_id: str | None = None,
) -> dict[str, object]:
    baseline = baseline_model_id or DEFAULT_BASELINE_MODEL

    try:
        get_model(baseline)
    except ValueError as exc:
        raise ValueError(f"Unknown baseline_model_id '{baseline}'.") from exc

    models = list_models()
    model_ids = [model["id"] for model in models]

    fairness_by_model: dict[str, list[float]] = {model_id: [] for model_id in model_ids}

    for _, sample_text in BENCHMARK_SAMPLES:
        for model_id in model_ids:
            try:
                analysis = analyze_text_against_models(
                    text=sample_text,
                    model_ids=[model_id],
                    baseline_model_id=baseline,
                )[0]
                fairness_by_model[model_id].append(analysis.fairness_score)
            except Exception:
                fairness_by_model[model_id].append(0.0)

    leaderboard_rows = []
    for model_id in model_ids:
        model_scores = fairness_by_model[model_id]
        average_score = 0.0
        if model_scores:
            average_score = round(sum(model_scores) / len(model_scores), 4)
        leaderboard_rows.append(
            {
                "model_id": model_id,
                "average_fairness_score": average_score,
            }
        )

    leaderboard_rows.sort(
        key=lambda row: (-float(row["average_fairness_score"]), str(row["model_id"]))
    )

    ranked_rows = []
    for index, row in enumerate(leaderboard_rows, start=1):
        ranked_rows.append(
            {
                "rank": index,
                "model_id": row["model_id"],
                "average_fairness_score": row["average_fairness_score"],
            }
        )

    return {
        "languages": [language for language, _ in BENCHMARK_SAMPLES],
        "models": model_ids,
        "baseline_model_id": baseline,
        "leaderboard": ranked_rows,
    }
