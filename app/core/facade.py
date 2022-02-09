from dataclasses import dataclass

from app.core.user.dto import UserRegisterRequest, UserRegisterResponse
from app.core.user.interactor import UserInteractor
from app.core.user.repository import IUserRepository


@dataclass
class WalletService:
    user_interactor: UserInteractor

    def register_user(self, user_request: UserRegisterRequest) -> UserRegisterResponse:
        user = self.user_interactor.register(user_request=user_request)
        return UserRegisterResponse.from_user(user)

    @classmethod
    def create(cls, user_repository: IUserRepository) -> "WalletService":
        user_interactor = UserInteractor(repository=user_repository)
        return cls(user_interactor=user_interactor)
