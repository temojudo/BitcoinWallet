import os

from fastapi import FastAPI

from app.core.facade import WalletService
from app.infra.currency_converter_strategy.default_currency_converter_strategy import (
    DefaultConverterStrategy,
)
from app.infra.factory.wallet import DefaultWalletFactory
from app.infra.fastapi.transaction_controller import transaction_api
from app.infra.fastapi.user_controller import user_api
from app.infra.fastapi.wallet_controller import wallet_api
from app.infra.fee_calculation_strategies.default_fee_calculation_strategy import (
    DefaultFeeCalculationStrategy,
)
from app.infra.sqlite.transaction_repository import SQLiteTransactionRepository
from app.infra.sqlite.user_repository import SQLiteUserRepository
from app.infra.sqlite.wallet_repository import SQLiteWalletRepository


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(user_api)
    app.include_router(wallet_api)
    app.include_router(transaction_api)

    db_filepath = f"{os.getcwd()}/db_test.db"

    app.state.core = WalletService.create(
        user_repository=SQLiteUserRepository(db_filepath),
        wallet_repository=SQLiteWalletRepository(db_filepath),
        wallet_factory=DefaultWalletFactory(),
        transaction_repository=SQLiteTransactionRepository(db_filepath),
        fee_calculation_strategy=DefaultFeeCalculationStrategy(),
        currency_converter_strategy=DefaultConverterStrategy(),
    )

    return app
