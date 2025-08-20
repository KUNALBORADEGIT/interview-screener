# models/question.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text
from engine.db.base import Base


class Question(Base):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)

    # Relationships
    jdtoqs: Mapped[list["JDToQS"]] = relationship("JDToQS", back_populates="question")
    interviews: Mapped[list["Interview"]] = relationship(
        "Interview", back_populates="question"
    )
