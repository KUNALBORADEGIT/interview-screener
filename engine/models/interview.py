from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text, String, Float
from engine.db.base import Base


class Interview(Base):
    __tablename__ = "interview"

    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("candidate.id"), nullable=False
    )
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"), nullable=False)
    transcript: Mapped[str] = mapped_column(Text, nullable=True)
    audio_url: Mapped[str] = mapped_column(String(255), nullable=True)
    score: Mapped[float] = mapped_column(Float, nullable=True)

    # Relationships
    candidate: Mapped["Candidate"] = relationship(
        "Candidate", back_populates="interviews"
    )
    question: Mapped["Question"] = relationship("Question", back_populates="interviews")
