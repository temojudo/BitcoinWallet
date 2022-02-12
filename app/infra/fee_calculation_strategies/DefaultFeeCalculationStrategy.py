from app.core.wallet.wallet import Wallet


class DefaultFeeCalculationStrategy:
    @classmethod
    def calculate_fee(cls, source_wallet: Wallet, destination_wallet: Wallet) -> float:
        return 0.015 if source_wallet.owner != destination_wallet.owner else 0.0
