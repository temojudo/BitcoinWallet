from app.core.http.exception import ApiException
from app.core.user.user import User
from app.infra.in_memory.storage import Storage


class InMemoryUserRepository:
    def __init__(self, storage: Storage) -> None:
        self.storage = storage
        self.id_seq = 0

    def save(self, user: User) -> User:
        user.id = self.id_seq
        self.id_seq += 1
        # if user.username in self.storage.users:
        #     raise ApiException("username already exists", status=400)
        self.storage.users[user.api_key] = user
        self.storage.wallets[user.api_key] = []
        return user

    def fetch_by_api_key(self, api_key: str) -> User:
        if api_key not in self.storage.users:
            raise ApiException("user not found", status=404)

        user = self.storage.users[api_key]
        user.wallets = self.storage.wallets[api_key]
        return user
