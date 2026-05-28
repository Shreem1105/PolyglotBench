from pydantic import BaseModel, field_validator


class AnalyzeRequest(BaseModel):
    text: str
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


class ModelAnalysis(BaseModel):
    model_id: str
    display_name: str
    provider: str
    token_count: int
    word_count: int
    character_count_no_spaces: int
    fertility: float
    token_multiplier: float
    estimated_attention_cost_multiplier: float
    estimated_latency_multiplier: float
    input_cost_estimate_usd: float
    fairness_score: float


class AnalyzeResponse(BaseModel):
    baseline_model_id: str
    text_preview: str
    analyses: list[ModelAnalysis]
