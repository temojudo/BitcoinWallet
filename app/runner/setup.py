import os

from fastapi import FastAPI

from app.core.facade import WalletService
from app.infra.factory.wallet import DefaultWalletFactory
from app.infra.fastapi.user_controller import user_api
from app.infra.fastapi.wallet_controller import wallet_api
from app.infra.sqlite.user_repository import SQLiteUserRepository
from app.infra.sqlite.wallet_repository import SQLiteWalletRepository


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(user_api)
    app.include_router(wallet_api)
    app.state.core = WalletService.create(
        user_repository=SQLiteUserRepository(f"{os.getcwd()}/db_test.db"),
        wallet_repository=SQLiteWalletRepository(f"{os.getcwd()}/db_test.db"),
        wallet_factory=DefaultWalletFactory(),
    )

    return app
