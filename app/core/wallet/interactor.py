from dataclasses import dataclass

from app.core.transaction.dto import MakeTransactionRequest
from app.core.user.interactor import UserInteractor
from app.core.wallet.dto import WalletCreateRequest
from app.core.wallet.factory import WalletFactory
from app.core.wallet.repository import IWalletRepository
from app.core.wallet.wallet import Wallet
from app.infra.http.exception import ApiException


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

    def make_transaction(self, request: MakeTransactionRequest) -> float:
        src_wallet = self.repository.fetch_by_wallet_address(request.source)
        if src_wallet.owner != request.api_key:
            raise ApiException("source wallet doesn't belong to issuer", status=401)

        dst_wallet = self.repository.fetch_by_wallet_address(request.destination)
        # TODO: check if null
        fee = 0.015 if dst_wallet.owner != request.api_key else 0.0

        if src_wallet.balance.btc >= request.amount:
            self.repository.update_balance(src_wallet, -request.amount)
            self.repository.update_balance(dst_wallet, request.amount * (1 - fee))
        else:
            raise ApiException("not enough balance")

        return fee
