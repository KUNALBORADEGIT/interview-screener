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
    app.mount(
        "/static",
        StaticFiles(directory=Path(settings.BASE_DIR) / "static"),
        name="static",
    )
