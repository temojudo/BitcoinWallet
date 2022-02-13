from typing import List

from app.core.http.exception import ApiException
from app.core.transaction.dto import Statistics
from app.core.transaction.transaction import Transaction
from app.infra.in_memory.storage import Storage


class InMemoryTransactionRepository:
    def __init__(self, storage: Storage):
        self.storage = storage
        self.id_seq = 0

    def save(self, transaction: Transaction) -> Transaction:
        raise ApiException("not implemented", status=403)

    def fetch_by_api_key(self, api_key: str) -> List[Transaction]:
        raise ApiException("not implemented", status=403)

    def query_statistics(self) -> Statistics:
        raise ApiException("not implemented", status=403)
