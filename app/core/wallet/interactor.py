from dataclasses import dataclass

from app.core.user.interactor import UserInteractor
from app.core.wallet.dto import WalletCreateRequest
from app.core.wallet.factory import WalletFactory
from app.core.wallet.repository import IWalletRepository
from app.core.wallet.wallet import Wallet


@dataclass
class WalletInteractor:
    repository: IWalletRepository
    user_interactor: UserInteractor
    factory: WalletFactory

    def create(self, wallet_request: WalletCreateRequest) -> Wallet:
        user = self.user_interactor.get_by_api_key(wallet_request.api_key)

        wallet = self.factory.create(user)
        self.repository.save(wallet)

        return wallet

    def make_transaction(
        self,
        source_wallet: Wallet,
        destination_wallet: Wallet,
        amount: float,
        fee: float,
    ) -> None:
        self.repository.update_balance(source_wallet, -(amount + fee))
        self.repository.update_balance(destination_wallet, amount)

    def get_by_wallet_address(self, wallet_address: str) -> Wallet:
        return self.repository.fetch_by_wallet_address(wallet_address)
