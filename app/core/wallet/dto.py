from dataclasses import dataclass

from app.core.wallet.currency_converter_strategy import CurrencyConverterName
from app.core.wallet.wallet import Wallet


@dataclass
class WalletCreateRequest:
    api_key: str


@dataclass
class WalletCreateResponse:
    address: str
    btc: float
    usd: float

    @classmethod
    def from_wallet(cls, wallet: Wallet) -> "WalletCreateResponse":
        return cls(
            address=wallet.address,
            btc=wallet.balance.btc,
            usd=wallet.get_converted_currency(CurrencyConverterName.BTC_TO_USD),
        )


@dataclass
class GetWalletRequest:
    api_key: str
    address: str


@dataclass
class GetWalletResponse:
    address: str
    btc: float
    usd: float

    @classmethod
    def from_wallet(cls, wallet: Wallet) -> "GetWalletResponse":
        return cls(
            address=wallet.address,
            btc=wallet.balance.btc,
            usd=wallet.get_converted_currency(CurrencyConverterName.BTC_TO_USD),
        )
