from fastapi import FastAPI

from app.api.routes_analyze import router as analyze_router
from app.api.routes_health import router as health_router
from app.api.routes_models import router as models_router

app = FastAPI(
    title="PolyglotBench API",
    version="0.1.0",
    description="Backend API for multilingual tokenization fairness analysis.",
)

app.include_router(health_router)
app.include_router(models_router)
app.include_router(analyze_router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "PolyglotBench API",
        "version": "0.1.0",
        "status": "running",
    }
