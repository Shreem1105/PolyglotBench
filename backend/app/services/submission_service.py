from sqlalchemy.orm import Session

from app.db.models import AnalysisSubmission
from app.schemas.analyze import AnalyzeResponse
from app.schemas.submissions import SubmissionResponse


def _to_submission_response(record: AnalysisSubmission) -> SubmissionResponse:
    selected_models = [item for item in record.selected_models.split(",") if item]
    return SubmissionResponse(
        id=record.id,
        text_preview=record.text_preview,
        language_detected=record.language_detected,
        selected_models=selected_models,
        baseline_model_id=record.baseline_model_id,
        min_fairness_score=record.min_fairness_score,
        max_token_multiplier=record.max_token_multiplier,
        created_at=record.created_at,
    )


def save_analysis_submission(
    db: Session,
    analyze_response: AnalyzeResponse,
    selected_model_ids: list[str],
) -> SubmissionResponse:
    analyses = analyze_response.analyses

    min_fairness_score = min((item.fairness_score for item in analyses), default=0.0)
    max_token_multiplier = max((item.token_multiplier for item in analyses), default=0.0)
    language_detected = analyses[0].language_detected if analyses else "unknown"

    record = AnalysisSubmission(
        text_preview=analyze_response.text_preview,
        language_detected=language_detected or "unknown",
        selected_models=",".join(selected_model_ids),
        baseline_model_id=analyze_response.baseline_model_id,
        min_fairness_score=round(float(min_fairness_score), 4),
        max_token_multiplier=round(float(max_token_multiplier), 4),
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return _to_submission_response(record)


def list_recent_submissions(db: Session, limit: int = 20) -> list[SubmissionResponse]:
    safe_limit = min(max(limit, 1), 100)

    records = (
        db.query(AnalysisSubmission)
        .order_by(AnalysisSubmission.created_at.desc())
        .limit(safe_limit)
        .all()
    )

    return [_to_submission_response(record) for record in records]
