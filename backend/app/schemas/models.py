from pydantic import BaseModel


class ModelInfo(BaseModel):
    id: str
    display_name: str
    provider: str
    tokenizer_type: str
    tokenizer_name: str
    input_price_per_million_tokens: float
    notes: str


class ModelsResponse(BaseModel):
    models: list[ModelInfo]
