from pydantic import BaseModel, field_validator

from app.schemas.analyze import ModelAnalysis


class CompareRequest(BaseModel):
    texts: list[str]
    model_ids: list[str]
    baseline_model_id: str | None = None

    @field_validator("model_ids")
    @classmethod
    def normalize_model_ids(cls, value: list[str]) -> list[str]:
        return [model_id.strip() for model_id in value]

    @field_validator("baseline_model_id")
    @classmethod
    def normalize_baseline_model_id(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None


class CompareTextResult(BaseModel):
    text_index: int
    text_preview: str
    baseline_model_id: str
    analyses: list[ModelAnalysis]


class CompareResponse(BaseModel):
    total_texts: int
    model_ids: list[str]
    baseline_model_id: str
    results: list[CompareTextResult]
