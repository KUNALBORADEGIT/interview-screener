# engine/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from engine.core.config import settings

engine = create_engine(settings.database_url, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to use in routes
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
