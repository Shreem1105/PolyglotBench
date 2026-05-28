from pydantic import BaseModel, field_validator


class ExportRequest(BaseModel):
    text: str
    model_ids: list[str]
    baseline_model_id: str | None = None
    format: str = "json"

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

    @field_validator("format")
    @classmethod
    def normalize_format(cls, value: str) -> str:
        return value.strip().lower()
