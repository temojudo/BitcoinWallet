from typing import List

from app.core.transaction.dto import Statistics
from app.core.transaction.transaction import Transaction
from app.infra.in_memory.storage import Storage


class InMemoryTransactionRepository:
    def __init__(self, storage: Storage):
        self.storage = storage
        self.id_seq = 0

    def save(self, transaction: Transaction) -> Transaction:
        self.id_seq += 1
        transaction.id = self.id_seq
        self.storage.transactions[transaction.id] = transaction
        return transaction

    def fetch_by_api_key(self, api_key: str) -> List[Transaction]:
        result: List[Transaction] = []

        wallets = self.storage.wallets[api_key]
        wallet_addresses = [wallet.address for wallet in wallets]

        for transaction_id in self.storage.transactions:
            transaction = self.storage.transactions[transaction_id]
            if (
                transaction.source in wallet_addresses
                or transaction.destination in wallet_addresses
            ):
                result.append(transaction)

        return result

    def query_statistics(self) -> Statistics:
        num_transactions = len(self.storage.transactions)
        profit = 0.0
        for transaction_id in self.storage.transactions:
            transaction = self.storage.transactions[transaction_id]
            profit += transaction.fee
        return Statistics(num_transactions=num_transactions, profit=profit)
