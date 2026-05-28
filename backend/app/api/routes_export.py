from typing import Any

from fastapi import APIRouter, HTTPException, Response

from app.core.config import DEFAULT_BASELINE_MODEL, PROJECT_NAME
from app.schemas.export import ExportRequest
from app.services.analysis_service import analyze_text_against_models
from app.services.export_service import analyses_to_csv

router = APIRouter()


def _to_http_exception(exc: Exception) -> HTTPException:
    message = str(exc)
    if message.startswith("Unknown model_id") or message.startswith("Unknown baseline_model_id"):
        return HTTPException(status_code=400, detail=message)
    return HTTPException(status_code=500, detail=message)


@router.post("/export", response_model=None)
def export_analysis(payload: ExportRequest) -> Any:
    text = payload.text

    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Text must not be empty or whitespace.")

    if not payload.model_ids:
        raise HTTPException(status_code=400, detail="model_ids must contain at least one model id.")

    if len(set(payload.model_ids)) != len(payload.model_ids):
        raise HTTPException(status_code=400, detail="model_ids must not contain duplicates.")

    if payload.format not in {"json", "csv"}:
        raise HTTPException(status_code=400, detail="format must be either 'json' or 'csv'.")

    baseline_model_id = payload.baseline_model_id or DEFAULT_BASELINE_MODEL

    try:
        analyses = analyze_text_against_models(
            text=text,
            model_ids=payload.model_ids,
            baseline_model_id=baseline_model_id,
        )
    except (ValueError, RuntimeError) as exc:
        raise _to_http_exception(exc) from exc

    if payload.format == "csv":
        csv_content = analyses_to_csv(analyses)
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="polyglotbench_export.csv"'},
        )

    return {
        "project": PROJECT_NAME,
        "export_format": "json",
        "baseline_model_id": baseline_model_id,
        "text_preview": text[:120],
        "analyses": [analysis.model_dump() for analysis in analyses],
    }
