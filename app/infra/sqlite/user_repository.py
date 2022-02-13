from sqlite3 import Error

from app.core.http.exception import ApiException
from app.core.user.user import User
from app.infra.sqlite.db_wrapper import SQLiteWrapper


class SQLiteUserRepository:
    def __init__(self, db_uri: str):
        self.db_uri = db_uri
        self._wrapper = SQLiteWrapper(db_uri)
        try:
            self._wrapper.create(CREATE_USER_TABLE_QUERY)
        except Error as e:
            raise ApiException(f"couldn't connect to database\nstacktrace: {e}")

    def save(self, user: User) -> User:
        query = INSERT_USER_QUERY

        if user.id != -1:
            raise ApiException("given already created user")

        db_user = self._wrapper.insert(query, "users", (user.username, user.api_key))

        if not db_user:
            raise ApiException("Database error", 505)

        return User.from_dao(db_user)

    def fetch_by_api_key(self, api_key: str) -> User:
        user = self._wrapper.select_all(FETCH_USER_QUERY, (api_key,))

        if not user:
            raise ApiException("Wrong api_key", 503)

        return User.from_joined_dao(user)


FETCH_USER_QUERY = """
        SELECT users.id as user_id, username, api_key, wallets.id as wallet_id, owner, address, btc FROM users
        LEFT JOIN  wallets ON users.api_key=wallets.owner
        WHERE users.api_key=?
"""

INSERT_USER_QUERY = """ INSERT INTO users(username, api_key)
                            VALUES (?,?)"""

CREATE_USER_TABLE_QUERY = """
                CREATE TABLE IF NOT EXISTS users (
                    id integer PRIMARY KEY,
                    username text NOT NULL UNIQUE,
                    api_key text NOT NULL UNIQUE
                );"""
