from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    text: str
    model_ids: list[str]
    baseline_model_id: str | None = None


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
