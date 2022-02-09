import sqlite3
from dataclasses import dataclass
from sqlite3 import Connection
from typing import Any, Optional


@dataclass
class SQLiteWrapper:
    db_file: str

    def get_connection(self) -> Connection:
        connection = sqlite3.connect(self.db_file)
        connection.row_factory = sqlite3.Row
        return connection

    def close_connection(self, connection: Connection) -> None:
        connection.close()

    def create_table(self, create_table_sql: str) -> None:
        conn = self.get_connection()
        conn.cursor().execute(create_table_sql)
        self.close_connection(conn)

    def fetch_all(
        self, query: str, connection: Connection, args: Optional[Any] = None
    ) -> Any:
        return self._execute_cursor(
            query=query, connection=connection, args=args
        ).fetchall()

    def fetch_one(
        self, query: str, connection: Connection, args: Optional[Any] = None
    ) -> Any:
        return self._execute_cursor(
            query=query, connection=connection, args=args
        ).fetchone()

    def execute(self, query: str, args: Any = None) -> Any:
        connection = self.get_connection()
        result = self._execute_cursor(
            query=query, connection=connection, args=args
        ).fetchone()
        connection.commit()
        connection.close()
        return result

    def _execute_cursor(
        self, query: str, connection: Connection, args: Optional[Any] = None
    ) -> Any:
        if args:
            return connection.cursor().execute(query, args)
        return connection.cursor().execute(query)
