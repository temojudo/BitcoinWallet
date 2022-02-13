from typing import Any, Dict

from app.core.wallet.balance import Balance
from app.core.wallet.currency_converter_strategy import CurrencyConverterName


class Wallet:
    def __init__(self, address: str, owner: str, balance: Balance):
        self.address = address
        self.owner = owner
        self.balance = balance
        self.id: int = -1

        self.converted_currencies: Dict[CurrencyConverterName, float] = {}

    def with_id(self, wallet_id: int) -> "Wallet":
        self.id = wallet_id
        return self

    def set_converted_currency(self, name: CurrencyConverterName, value: float) -> None:
        self.converted_currencies[name] = value

    def get_converted_currency(self, name: CurrencyConverterName) -> float:
        return self.converted_currencies[name]

    @classmethod
    def from_dao(cls, db_wallet: Dict[str, Any]) -> "Wallet":
        wallet = cls(
            owner=db_wallet["owner"],
            address=db_wallet["address"],
            balance=Balance(btc=db_wallet["btc"]),
        )
        wallet.id = db_wallet["id"]
        return wallet
