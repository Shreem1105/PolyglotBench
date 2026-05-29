from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class AnalysisSubmission(Base):
    __tablename__ = "analysis_submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    text_preview: Mapped[str] = mapped_column(String(120), nullable=False)
    language_detected: Mapped[str] = mapped_column(String(32), nullable=False, default="unknown")
    selected_models: Mapped[str] = mapped_column(String(512), nullable=False)
    baseline_model_id: Mapped[str] = mapped_column(String(100), nullable=False)
    min_fairness_score: Mapped[float] = mapped_column(Float, nullable=False)
    max_token_multiplier: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
