from dataclasses import dataclass

from app.core.user.dto import UserRegisterRequest, UserRegisterResponse
from app.core.user.interactor import UserInteractor
from app.core.user.repository import IUserRepository
from app.core.wallet.dto import WalletCreateRequest, WalletCreateResponse
from app.core.wallet.factory import WalletFactory
from app.core.wallet.interactor import WalletInteractor
from app.core.wallet.repository import IWalletRepository


@dataclass
class WalletService:
    user_interactor: UserInteractor
    wallet_interactor: WalletInteractor

    def register_user(self, user_request: UserRegisterRequest) -> UserRegisterResponse:
        user = self.user_interactor.register(user_request=user_request)
        return UserRegisterResponse.from_user(user)

    def create_wallet(
        self, wallet_request: WalletCreateRequest
    ) -> WalletCreateResponse:
        wallet = self.wallet_interactor.create(wallet_request)
        return WalletCreateResponse.from_wallet(wallet)

    @classmethod
    def create(
        cls,
        user_repository: IUserRepository,
        wallet_repository: IWalletRepository,
        wallet_factory: WalletFactory,
    ) -> "WalletService":
        user_interactor = UserInteractor(repository=user_repository)
        wallet_interactor = WalletInteractor(
            repository=wallet_repository,
            user_interactor=user_interactor,
            factory=wallet_factory,
        )
        return cls(user_interactor=user_interactor, wallet_interactor=wallet_interactor)
