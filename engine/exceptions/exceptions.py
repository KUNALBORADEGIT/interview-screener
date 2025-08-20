from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from engine.core import logger


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(ValueError)
    async def handle_value_error(request: Request, exc: ValueError):
        logger.error(f"❌ ValueError: {exc} at {request.url}")
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )
