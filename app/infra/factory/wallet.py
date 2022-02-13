from dataclasses import dataclass

from app.core import UUIDAdapter
from app.core.http.exception import ApiException
from app.core.user.user import User
from app.core.wallet.balance import Balance
from app.core.wallet.factory import WalletFactory
from app.core.wallet.wallet import Wallet


@dataclass
class DefaultWalletFactory(WalletFactory):
    WALLET_LIMIT = 3

    def create(self, user: User) -> Wallet:
        wallets = user.wallets

        if len(wallets) >= self.WALLET_LIMIT:
            raise ApiException("Wallet limit exceeded")

        return Wallet(
            address=UUIDAdapter.generate_address(),
            balance=Balance(btc=1),
            owner=user.api_key,
        )
