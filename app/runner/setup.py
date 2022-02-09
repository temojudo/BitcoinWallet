import os

from fastapi import FastAPI

from app.core.facade import WalletService
from app.infra.fastapi.user_controller import user_api
from app.infra.in_memory.user_repository import InMemoryUserRepository
from app.infra.sqlite.user_repository import SQLiteUserRepository


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(user_api)
    app.state.core = WalletService.create(
        user_repository=SQLiteUserRepository(f"{os.getcwd()}/db_test.db")
    )

    return app
