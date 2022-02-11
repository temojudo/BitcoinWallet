from dataclasses import dataclass
from typing import Any, Dict, Optional

from app.core.wallet.balance import Balance


class Wallet:
    def __init__(self, address: str, owner: str, balance: Balance):
        self.address = address
        self.owner = owner
        self.balance = balance
        self.id: int = -1

    def with_id(self, wallet_id: int) -> "Wallet":
        self.id = wallet_id
        return self

    @classmethod
    def from_dao(cls, db_wallet: Dict[str, Any]) -> "Wallet":
        wallet = cls(
            owner=db_wallet["owner"],
            address=db_wallet["address"],
            balance=Balance(btc=db_wallet["btc"]),
        )
        wallet.id = db_wallet["id"]
        return wallet
