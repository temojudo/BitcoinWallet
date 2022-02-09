from fastapi import FastAPI

from app.core.facade import WalletService
from app.infra.fastapi.user_controller import user_api
from app.infra.in_memory.user_repository import InMemoryUserRepository


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(user_api)
    app.state.core = WalletService.create(user_repository=InMemoryUserRepository())

    return app
