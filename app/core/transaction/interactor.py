from dataclasses import dataclass
from typing import List

from app.core import ADMIN_API_KEY
from app.core.http.exception import ApiException
from app.core.transaction.dto import (
    GetTransactionsRequest,
    MakeTransactionRequest,
    Statistics,
)
from app.core.transaction.fee_calculation_strategy import IFeeCalculationStrategy
from app.core.transaction.repository import ITransactionRepository
from app.core.transaction.transaction import Transaction
from app.core.wallet.interactor import WalletInteractor


@dataclass
class TransactionInteractor:
    repository: ITransactionRepository
    wallet_interactor: WalletInteractor
    fee_calculation_strategy: IFeeCalculationStrategy

    def make_transaction(self, request: MakeTransactionRequest) -> Transaction:
        source_wallet = self.wallet_interactor.get_by_wallet_address(request.source)
        destination_wallet = self.wallet_interactor.get_by_wallet_address(
            request.destination
        )

        if source_wallet.owner != request.api_key:
            raise ApiException("Source wallet doesn't belong to issuer", status=401)

        if source_wallet.balance.btc < request.amount:
            raise ApiException("Insufficient balance", status=400)

        fee = self.fee_calculation_strategy.calculate_fee(
            source_wallet, destination_wallet
        )

        transaction = Transaction(
            request.source,
            request.destination,
            request.amount * (1 - fee),
            request.amount * fee,
        )

        self.wallet_interactor.make_transaction(transaction)

        return self.repository.save(transaction)

    def get_transactions(self, request: GetTransactionsRequest) -> List[Transaction]:
        return self.repository.fetch_by_api_key(request.api_key)

    def get_statistics(self, api_key: str) -> Statistics:
        if ADMIN_API_KEY != api_key:
            raise ApiException("invalid api key", status=401)
        return self.repository.query_statistics()
