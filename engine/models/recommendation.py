from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Float, String
from engine.db.base import Base


class Recommendation(Base):
    __tablename__ = "recommendation"

    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("candidate.id"), unique=True, nullable=False
    )
    overall_score: Mapped[float] = mapped_column(Float, nullable=False)
    recommendation: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # e.g., "hire", "reject"

    # Relationships
    candidate: Mapped["Candidate"] = relationship(
        "Candidate", back_populates="recommendation"
    )
