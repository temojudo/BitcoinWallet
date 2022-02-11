from typing import Any, Dict, List

from app.core.wallet.balance import Balance
from app.core.wallet.wallet import Wallet
from app.infra.http.exception import ApiException


class User:
    def __init__(self, username: str, api_key: str):
        self.username = username
        self.api_key = api_key
        self.wallets: List[Wallet] = []
        self.id: int = -1

    @classmethod
    def from_dao(cls, db_user: Dict[str, Any]) -> "User":
        user = cls(
            username=db_user["username"],
            api_key=db_user["api_key"],
        )
        user.id = db_user["id"]
        return user

    @classmethod
    def from_joined_dao(cls, db_user: List[Dict[str, Any]]) -> "User":
        if len(db_user) == 0:
            raise ApiException("couldn't fetch user")
        user_info = db_user[0]
        result = cls(
            username=user_info["username"],
            api_key=user_info["api_key"],
        )
        result.id = user_info["user_id"]
        result.wallets = [
            Wallet(
                address=wallet["address"],
                balance=Balance(btc=wallet["btc"]),
                owner=wallet["owner"],
            ).with_id(wallet["wallet_id"])
            for wallet in db_user
        ]
        return result
