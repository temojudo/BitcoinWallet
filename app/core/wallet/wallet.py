from dataclasses import dataclass
from typing import Any, Dict, Optional

from app.core.wallet.balance import Balance


@dataclass
class Wallet:
    address: str
    owner: str
    balance: Balance
    id: Optional[int] = None

    @classmethod
    def from_dao(cls, db_user: Dict[str, Any]) -> "Wallet":
        return cls(
            id=db_user["id"],
            owner=db_user["owner"],
            address=db_user["address"],
            balance=Balance(btc=db_user["btc"]),
        )
