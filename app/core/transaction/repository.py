from typing import Protocol

from app.core.transaction.transaction import Transaction


class ITransactionRepository(Protocol):
    def save(self, transaction: Transaction) -> Transaction:
        pass
