from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import as_declarative, declared_attr, Mapped, mapped_column


@as_declarative()
class Base:
    # Common fields for all tables
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Auto-generate table name from class name
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
