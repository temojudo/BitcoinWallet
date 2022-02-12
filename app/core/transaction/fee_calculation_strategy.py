from typing import Protocol

from app.core.wallet.wallet import Wallet


class IFeeCalculationStrategy(Protocol):
    def calculate_fee(self, source_wallet: Wallet, destination_wallet: Wallet) -> float:
        pass
