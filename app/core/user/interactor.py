from dataclasses import dataclass

from app.core import UUIDAdapter
from app.core.user.dto import UserRegisterRequest
from app.core.user.repository import IUserRepository
from app.core.user.user import User


@dataclass
class UserInteractor:
    repository: IUserRepository

    def register(self, user_request: UserRegisterRequest) -> User:
        user = User(
            username=user_request.username, api_key=UUIDAdapter.generate_api_key()
        )
        return self.repository.save(user)

    def get_by_api_key(self, api_key: str) -> User:
        return self.repository.fetch_by_api_key(api_key)
