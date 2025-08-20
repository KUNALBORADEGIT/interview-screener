from fastapi import FastAPI
from engine.core import logger


def register_events(app: FastAPI):
    @app.on_event("startup")
    async def startup():
        logger.info("🚀 FastAPI started")

    @app.on_event("shutdown")
    async def shutdown():
        logger.info("🛑 FastAPI shutdown")
