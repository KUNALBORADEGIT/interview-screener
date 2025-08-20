# models/jdtoqs.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from engine.db.base import Base


class JDToQS(Base):
    __tablename__ = "jdtoqs"

    jd_id: Mapped[int] = mapped_column(ForeignKey("jobdescription.id"), nullable=False)
    qs_id: Mapped[int] = mapped_column(ForeignKey("question.id"), nullable=False)

    # Relationships
    jobdescription: Mapped["JobDescription"] = relationship(
        "JobDescription", back_populates="jdtoqs"
    )
    question: Mapped["Question"] = relationship("Question", back_populates="jdtoqs")
