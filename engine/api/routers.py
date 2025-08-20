# engine/api/routers.py
from fastapi import FastAPI
from engine.routes import candidate, interview, jobdescription, twiml
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from engine.core.config import settings


def include_routers(app: FastAPI):

    app.include_router(
        jobdescription.router, prefix="/jobdescription", tags=["jobdescription"]
    )
    app.include_router(candidate.router, prefix="/candidates", tags=["candidates"])
    app.include_router(interview.router, prefix="/interview", tags=["interview"])
    app.include_router(twiml.router, prefix="/twiml", tags=["twiml"])

    # Ensure static folder exists (auto-create if missing)
    static_path = Path(settings.BASE_DIR) / "static"
    static_path.mkdir(parents=True, exist_ok=True)

    # Mount static files
    app.mount("/static", StaticFiles(directory=static_path), name="static")
