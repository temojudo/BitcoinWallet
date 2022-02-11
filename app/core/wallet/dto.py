from dataclasses import dataclass

from app.core.wallet.balance import Balance
from app.core.wallet.wallet import Wallet


@dataclass
class WalletCreateRequest:
    api_key: str


@dataclass
class WalletCreateResponse:
    address: str
    usd: float
    btc: float

    @classmethod
    def from_wallet(cls, wallet: Wallet) -> "WalletCreateResponse":
        return cls(
            address=wallet.address, btc=wallet.balance.btc, usd=wallet.balance.btc
        )
