from fastapi import APIRouter

from app.core.model_registry import list_models
from app.schemas.models import ModelsResponse

router = APIRouter()


@router.get("/models", response_model=ModelsResponse)
def get_models() -> ModelsResponse:
    models = list_models()
    return ModelsResponse(models=models)
