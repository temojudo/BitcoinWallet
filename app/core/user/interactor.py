import uuid
from dataclasses import dataclass

from app.core.user.dto import UserRegisterRequest
from app.core.user.repository import IUserRepository
from app.core.user.user import User
from app.infra.in_memory.user_repository import InMemoryUserRepository


@dataclass
class UserInteractor:
    repository: IUserRepository = InMemoryUserRepository()

    def register(self, user_request: UserRegisterRequest) -> User:
        # TODO: create user correctly
        user = User(username=user_request.username, api_key=str(uuid.uuid4()))
        return self.repository.save(user)
