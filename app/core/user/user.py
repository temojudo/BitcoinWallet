from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.core.wallet.balance import Balance
from app.core.wallet.wallet import Wallet
from app.infra.http.exception import ApiException


@dataclass
class User:
    username: str
    api_key: str
    wallets: List[Wallet] = field(default_factory=list)
    id: Optional[int] = None

    @classmethod
    def from_dao(cls, db_user: Dict[str, Any]) -> "User":
        return cls(
            id=db_user["id"],
            username=db_user["username"],
            api_key=db_user["api_key"],
        )

    @classmethod
    def from_joined_dao(cls, db_user: List[Dict[str, Any]]) -> "User":
        if len(db_user) == 0:
            raise ApiException("couldn't fetch user")
        user_info = db_user[0]
        result = cls(
            id=user_info["id"],
            username=user_info["username"],
            api_key=user_info["api_key"],
            wallets=[
                Wallet(
                    address=wallet["address"],
                    balance=Balance(btc=wallet["btc"]),
                    id=5,
                    owner=wallet["owner"],
                )
                for wallet in db_user
            ],
        )
        return result
