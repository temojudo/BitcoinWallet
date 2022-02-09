import sqlite3
from sqlite3 import Error

from app.core.user.user import User
from app.infra.http.exception import ApiException
from app.infra.sqlite.db_wrapper import SQLiteWrapper


class SQLiteUserRepository:
    def __init__(self, db_uri: str):
        self.db_uri = db_uri
        self._wrapper = SQLiteWrapper(db_uri)
        self._prepare_queries()
        try:
            self._wrapper.create_table(self._create_user_table)
        except Error as e:
            raise ApiException(f"couldn't connect to database\nstacktrace: {e}")

    def save(self, user: User) -> User:
        query = """ INSERT INTO users(username, api_key)
                            VALUES (?,?)"""

        if user.id is not None:
            raise ApiException("given already created user")

        db_user = self._wrapper.execute(query, (user.username, user.api_key))
        return User.from_dao(db_user)

    def _prepare_queries(self) -> None:
        self._create_user_table = """
                CREATE TABLE IF NOT EXISTS users (
                    id integer PRIMARY KEY,
                    username text NOT NULL UNIQUE,
                    api_key text NOT NULL UNIQUE
                );
        """
