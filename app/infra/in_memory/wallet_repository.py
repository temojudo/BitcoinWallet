from typing import List

from app.core.http.exception import ApiException
from app.core.transaction.transaction import Transaction
from app.core.wallet.wallet import Wallet
from app.infra.in_memory.storage import Storage


class InMemoryWalletRepository:
    def __init__(self, storage: Storage):
        self.storage = storage
        self.id_seq = 0

    def save(self, wallet: Wallet) -> Wallet:
        raise ApiException("not implemented", status=403)

    def fetch_by_wallet_address(self, address: str) -> Wallet:
        raise ApiException("not implemented", status=403)

    def update_balance(self, wallet_address: str, amount: float) -> Wallet:
        raise ApiException("not implemented", status=403)

    def get_wallet_transactions(self, address: str) -> List[Transaction]:
        raise ApiException("not implemented", status=403)
