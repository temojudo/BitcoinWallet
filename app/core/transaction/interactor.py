from dataclasses import dataclass
from typing import List

from app.core.transaction.dto import GetTransactionsRequest, MakeTransactionRequest
from app.core.transaction.repository import ITransactionRepository
from app.core.transaction.transaction import Transaction
from app.core.wallet.interactor import WalletInteractor


@dataclass
class TransactionInteractor:
    repository: ITransactionRepository
    wallet_interactor: WalletInteractor

    def make_transaction(self, request: MakeTransactionRequest) -> Transaction:
        # TODO: logic from wallet_interactor to calculate fee
        fee = self.wallet_interactor.make_transaction(request)
        transaction = Transaction(
            request.source,
            request.destination,
            request.amount * (1 - fee),
            request.amount * fee,
        )
        return self.repository.save(transaction)

    def get_transactions(self, request: GetTransactionsRequest) -> List[Transaction]:
        return self.repository.fetch_by_api_key(request.api_key)
