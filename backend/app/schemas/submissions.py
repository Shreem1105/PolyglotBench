from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SubmissionCreate(BaseModel):
    text_preview: str
    language_detected: str
    selected_models: list[str]
    baseline_model_id: str
    min_fairness_score: float
    max_token_multiplier: float


class SubmissionResponse(SubmissionCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SubmissionsResponse(BaseModel):
    submissions: list[SubmissionResponse]
