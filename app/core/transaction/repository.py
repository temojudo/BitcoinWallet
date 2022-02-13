from typing import List, Protocol

from app.core.transaction.dto import Statistics
from app.core.transaction.transaction import Transaction


class ITransactionRepository(Protocol):
    def save(self, transaction: Transaction) -> Transaction:
        pass

    def fetch_by_api_key(self, api_key: str) -> List[Transaction]:
        pass

    def query_statistics(self) -> Statistics:
        pass
