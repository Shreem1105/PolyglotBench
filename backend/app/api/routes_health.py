from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.db.database import SessionLocal

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "polyglotbench-backend",
    }


@router.get("/ready")
def ready() -> dict[str, str]:
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
    except Exception as exc:
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "database": "error",
                "detail": str(exc),
            },
        )
    finally:
        db.close()

    return {
        "status": "ready",
        "database": "ok",
        "service": "polyglotbench-backend",
    }
