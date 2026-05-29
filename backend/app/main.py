from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_analyze import router as analyze_router
from app.api.routes_compare import router as compare_router
from app.api.routes_export import router as export_router
from app.api.routes_health import router as health_router
from app.api.routes_leaderboard import router as leaderboard_router
from app.api.routes_models import router as models_router
from app.api.routes_submissions import router as submissions_router
from app.core.config import API_VERSION, PROJECT_NAME, get_cors_origins
from app.db import models as db_models
from app.db.database import Base, engine

app = FastAPI(
    title=f"{PROJECT_NAME} API",
    version=API_VERSION,
    description="Backend API for multilingual tokenization fairness analysis.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    _ = db_models
    Base.metadata.create_all(bind=engine)


app.include_router(health_router)
app.include_router(models_router)
app.include_router(analyze_router)
app.include_router(compare_router)
app.include_router(export_router)
app.include_router(leaderboard_router)
app.include_router(submissions_router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": f"{PROJECT_NAME} API",
        "version": API_VERSION,
        "status": "running",
    }
