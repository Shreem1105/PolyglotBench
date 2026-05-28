from fastapi import APIRouter, HTTPException

from app.core.config import DEFAULT_BASELINE_MODEL
from app.schemas.compare import CompareRequest, CompareResponse, CompareTextResult
from app.services.analysis_service import analyze_text_against_models

router = APIRouter()


def _to_http_exception(exc: Exception) -> HTTPException:
    message = str(exc)
    if message.startswith("Unknown model_id") or message.startswith("Unknown baseline_model_id"):
        return HTTPException(status_code=400, detail=message)
    return HTTPException(status_code=500, detail=message)


@router.post("/compare", response_model=CompareResponse)
def compare_texts(payload: CompareRequest) -> CompareResponse:
    if not payload.texts:
        raise HTTPException(status_code=400, detail="texts must contain at least one text sample.")

    for index, text in enumerate(payload.texts):
        if not text or not text.strip():
            raise HTTPException(
                status_code=400,
                detail=f"texts[{index}] must not be empty or whitespace.",
            )

    if not payload.model_ids:
        raise HTTPException(status_code=400, detail="model_ids must contain at least one model id.")

    if len(set(payload.model_ids)) != len(payload.model_ids):
        raise HTTPException(status_code=400, detail="model_ids must not contain duplicates.")

    baseline_model_id = payload.baseline_model_id or DEFAULT_BASELINE_MODEL

    results: list[CompareTextResult] = []
    for index, text in enumerate(payload.texts):
        try:
            analyses = analyze_text_against_models(
                text=text,
                model_ids=payload.model_ids,
                baseline_model_id=baseline_model_id,
            )
        except (ValueError, RuntimeError) as exc:
            raise _to_http_exception(exc) from exc

        results.append(
            CompareTextResult(
                text_index=index,
                text_preview=text[:120],
                baseline_model_id=baseline_model_id,
                analyses=analyses,
            )
        )

    return CompareResponse(
        total_texts=len(payload.texts),
        model_ids=payload.model_ids,
        baseline_model_id=baseline_model_id,
        results=results,
    )
