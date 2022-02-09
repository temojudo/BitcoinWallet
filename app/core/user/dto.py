from dataclasses import dataclass

from app.core.user.user import User


@dataclass
class UserRegisterRequest:
    username: str


@dataclass
class UserRegisterResponse:
    username: str
    api_key: str

    @classmethod
    def from_user(cls, user: User) -> "UserRegisterResponse":
        return cls(username=user.username, api_key=user.api_key)
