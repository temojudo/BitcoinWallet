from abc import ABC, abstractmethod

from app.core.user.user import User
from app.core.wallet.wallet import Wallet


class WalletFactory(ABC):
    @abstractmethod
    def create(self, user: User) -> Wallet:
        pass
