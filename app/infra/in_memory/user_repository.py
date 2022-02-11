from dataclasses import dataclass, field
from typing import Dict

from app.core.user.user import User


@dataclass
class InMemoryUserRepository:
    storage: Dict[str, User] = field(default_factory=dict)

    def save(self, user: User) -> User:
        self.storage[user.username] = user
        return user

    def fetch_by_api_key(self, api_key: str) -> User:
        pass
