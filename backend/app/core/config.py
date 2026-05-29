import os

from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME = os.getenv("PROJECT_NAME", "PolyglotBench")
API_VERSION = os.getenv("API_VERSION", "0.1.0")
DEFAULT_BASELINE_MODEL = os.getenv("DEFAULT_BASELINE_MODEL", "gpt-4o-mini")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./polyglotbench.db")
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000",
)
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")


def get_cors_origins() -> list[str]:
    return [origin.strip() for origin in CORS_ORIGINS.split(",") if origin.strip()]
