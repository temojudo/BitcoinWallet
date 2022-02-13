from dataclasses import dataclass
from typing import List

from app.core.transaction.dto import (
    GetTransactionsRequest,
    MakeTransactionRequest,
    Statistics,
    TransactionResponse,
)
from app.core.transaction.fee_calculation_strategy import IFeeCalculationStrategy
from app.core.transaction.interactor import TransactionInteractor
from app.core.transaction.repository import ITransactionRepository
from app.core.user.dto import UserRegisterRequest, UserRegisterResponse
from app.core.user.interactor import UserInteractor
from app.core.user.repository import IUserRepository
from app.core.wallet.currency_converter_strategy import ICurrencyConverterStrategy
from app.core.wallet.dto import (
    GetWalletRequest,
    GetWalletResponse,
    WalletCreateRequest,
    WalletCreateResponse,
)
from app.core.wallet.factory import WalletFactory
from app.core.wallet.interactor import WalletInteractor
from app.core.wallet.repository import IWalletRepository


@dataclass
class WalletService:
    user_interactor: UserInteractor
    wallet_interactor: WalletInteractor
    transaction_interactor: TransactionInteractor

    def register_user(self, user_request: UserRegisterRequest) -> UserRegisterResponse:
        user = self.user_interactor.register(user_request=user_request)
        return UserRegisterResponse.from_user(user)

    def create_wallet(
        self, wallet_request: WalletCreateRequest
    ) -> WalletCreateResponse:
        wallet = self.wallet_interactor.create(wallet_request)
        return WalletCreateResponse.from_wallet(wallet)

    def get_wallet(self, wallet_request: GetWalletRequest) -> GetWalletResponse:
        wallet = self.wallet_interactor.get(wallet_request)
        return GetWalletResponse.from_wallet(wallet)

    def make_transaction(
        self, transaction_request: MakeTransactionRequest
    ) -> TransactionResponse:
        transaction = self.transaction_interactor.make_transaction(transaction_request)
        return TransactionResponse.from_transaction(transaction)

    def get_transactions(
        self, transaction_request: GetTransactionsRequest
    ) -> List[TransactionResponse]:
        transactions = self.transaction_interactor.get_transactions(transaction_request)
        return [
            TransactionResponse.from_transaction(transaction)
            for transaction in transactions
        ]

    def get_wallet_transactions(
        self, address: str, api_key: str
    ) -> List[TransactionResponse]:
        transactions = self.wallet_interactor.get_wallet_transactions(address, api_key)
        return [
            TransactionResponse.from_transaction(transaction)
            for transaction in transactions
        ]

    def get_statistics(self, api_key: str) -> Statistics:
        return self.transaction_interactor.get_statistics(api_key)

    @classmethod
    def create(
        cls,
        user_repository: IUserRepository,
        wallet_repository: IWalletRepository,
        wallet_factory: WalletFactory,
        transaction_repository: ITransactionRepository,
        fee_calculation_strategy: IFeeCalculationStrategy,
        currency_converter_strategy: ICurrencyConverterStrategy,
    ) -> "WalletService":
        user_interactor = UserInteractor(repository=user_repository)
        wallet_interactor = WalletInteractor(
            repository=wallet_repository,
            user_interactor=user_interactor,
            factory=wallet_factory,
            currency_converter_strategy=currency_converter_strategy,
        )
        transaction_interactor = TransactionInteractor(
            repository=transaction_repository,
            wallet_interactor=wallet_interactor,
            fee_calculation_strategy=fee_calculation_strategy,
        )
        return cls(
            user_interactor=user_interactor,
            wallet_interactor=wallet_interactor,
            transaction_interactor=transaction_interactor,
        )
