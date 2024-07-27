from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from backend.app.api.exc_handlers import init_exc_handlers
from backend.app.api.routers import auth_router, todo_router, user_router
from backend.app.infra.ioc import create_container


def init_di(app: FastAPI) -> None:
    container = create_container()
    setup_dishka(container, app)


def init_routers(app: FastAPI) -> None:
    app.include_router(user_router)
    app.include_router(auth_router)
    app.include_router(todo_router)


def app_factory() -> FastAPI:
    app = FastAPI()

    init_di(app)
    init_routers(app)
    init_exc_handlers(app)

    return app
