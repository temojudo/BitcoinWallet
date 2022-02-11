import uuid
from dataclasses import dataclass

from app.core.user.user import User
from app.core.wallet.balance import Balance
from app.core.wallet.factory import WalletFactory
from app.core.wallet.wallet import Wallet
from app.infra.http.exception import ApiException


@dataclass
class DefaultWalletFactory(WalletFactory):
    WALLET_LIMIT = 3

    def create(self, user: User) -> Wallet:
        wallets = user.wallets

        if len(wallets) >= self.WALLET_LIMIT:
            raise ApiException("Wallet limit exceeded")

        return Wallet(
            address=str(uuid.uuid4()), balance=Balance(btc=1), owner=user.api_key
        )
