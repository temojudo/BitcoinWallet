from typing import List, Protocol

from app.core.transaction.transaction import Transaction
from app.core.wallet.wallet import Wallet


class IWalletRepository(Protocol):
    def save(self, wallet: Wallet) -> Wallet:
        pass

    def fetch_by_wallet_address(self, address: str) -> Wallet:
        pass

    def update_balance(self, wallet_address: str, amount: float) -> Wallet:
        pass

    def get_wallet_transactions(self, address: str) -> List[Transaction]:
        pass
