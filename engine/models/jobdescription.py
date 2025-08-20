# models/jobdescription.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text
from engine.db.base import Base


class JobDescription(Base):
    __tablename__ = "jobdescription"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    jobdescription: Mapped[str] = mapped_column(Text, nullable=False)

    # Relationships
    jdtoqs: Mapped[list["JDToQS"]] = relationship(
        "JDToQS", back_populates="jobdescription"
    )
