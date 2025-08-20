from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from engine.db.base import Base


class Candidate(Base):
    __tablename__ = "candidate"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    resume_url: Mapped[str] = mapped_column(String(255), nullable=True)

    # Relationships
    recommendation: Mapped["Recommendation"] = relationship(
        "Recommendation",
        back_populates="candidate",
        uselist=False,
        cascade="all, delete-orphan",
    )
    interviews: Mapped[list["Interview"]] = relationship(
        "Interview", back_populates="candidate", cascade="all, delete-orphan"
    )
