from typing import Protocol

from app.core.user.user import User


class IUserRepository(Protocol):
    def save(self, user: User) -> User:
        pass
