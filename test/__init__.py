from app.core.facade import WalletService
from app.infra.currency_converter_strategy.default_currency_converter_strategy import (
    DefaultConverterStrategy,
)
from app.infra.factory.wallet import DefaultWalletFactory
from app.infra.fee_calculation_strategies.default_fee_calculation_strategy import (
    DefaultFeeCalculationStrategy,
)
from app.infra.in_memory.storage import Storage
from app.infra.in_memory.transaction_repository import InMemoryTransactionRepository
from app.infra.in_memory.user_repository import *
from app.infra.in_memory.wallet_repository import InMemoryWalletRepository


# injects in memory implementations into facade
def create_facade() -> WalletService:
    storage = Storage()
    service = WalletService.create(
        user_repository=InMemoryUserRepository(storage),
        wallet_repository=InMemoryWalletRepository(storage),
        wallet_factory=DefaultWalletFactory(),
        currency_converter_strategy=DefaultConverterStrategy(),
        transaction_repository=InMemoryTransactionRepository(storage),
        fee_calculation_strategy=DefaultFeeCalculationStrategy(),
    )
    return service
