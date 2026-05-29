from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.config import DEFAULT_BASELINE_MODEL
from app.db.database import get_db
from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse
from app.schemas.submissions import SubmissionResponse, SubmissionsResponse
from app.services.analysis_service import analyze_text_against_models
from app.services.submission_service import list_recent_submissions, save_analysis_submission

router = APIRouter()


def _to_http_exception(exc: Exception) -> HTTPException:
    message = str(exc)
    if message.startswith("Unknown model_id") or message.startswith("Unknown baseline_model_id"):
        return HTTPException(status_code=400, detail=message)
    return HTTPException(status_code=500, detail=message)


@router.post(
    "/submissions/from-analysis",
    response_model=SubmissionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_submission_from_analysis(
    payload: AnalyzeRequest,
    db: Session = Depends(get_db),
) -> SubmissionResponse:
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

    analyze_response = AnalyzeResponse(
        baseline_model_id=baseline_model_id,
        text_preview=text[:120],
        analyses=analyses,
    )

    return save_analysis_submission(
        db=db,
        analyze_response=analyze_response,
        selected_model_ids=payload.model_ids,
    )


@router.get("/submissions", response_model=SubmissionsResponse)
def get_submissions(
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> SubmissionsResponse:
    submissions = list_recent_submissions(db=db, limit=limit)
    return SubmissionsResponse(submissions=submissions)
