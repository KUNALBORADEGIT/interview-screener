from fastapi import FastAPI
from engine.api import include_routers
from engine.middlewares import add_middlewares
from engine.events import register_events
from engine.exceptions import add_exception_handlers

from engine.routes import llm_test


def create_app() -> FastAPI:
    app = FastAPI(title="Server", version="1.0.0", docs_url="/docs", redoc_url="/redoc")

    # Core setup
    add_middlewares(app)
    add_exception_handlers(app)
    register_events(app)
    include_routers(app)
    app.include_router(llm_test.router)

    return app


app = create_app()
