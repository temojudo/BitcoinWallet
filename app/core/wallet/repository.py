from typing import Protocol

from app.core.wallet.wallet import Wallet


class IWalletRepository(Protocol):
    def save(self, wallet: Wallet) -> Wallet:
        pass
