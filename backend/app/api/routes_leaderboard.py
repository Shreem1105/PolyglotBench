from fastapi import APIRouter, HTTPException

from app.services.leaderboard_service import generate_fairness_leaderboard

router = APIRouter()


@router.get("/leaderboard")
def get_leaderboard() -> dict[str, object]:
    try:
        return generate_fairness_leaderboard()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
