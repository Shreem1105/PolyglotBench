from fastapi import APIRouter, HTTPException

from app.core.config import DEFAULT_BASELINE_MODEL
from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse
from app.services.analysis_service import analyze_text_against_models

router = APIRouter()


def _to_http_exception(exc: Exception) -> HTTPException:
    message = str(exc)
    if message.startswith("Unknown model_id") or message.startswith("Unknown baseline_model_id"):
        return HTTPException(status_code=400, detail=message)
    return HTTPException(status_code=500, detail=message)


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
        analyses = analyze_text_against_models(
            text=text,
            model_ids=payload.model_ids,
            baseline_model_id=baseline_model_id,
        )
    except (ValueError, RuntimeError) as exc:
        raise _to_http_exception(exc) from exc

    return AnalyzeResponse(
        baseline_model_id=baseline_model_id,
        text_preview=text[:120],
        analyses=analyses,
    )
