import sqlite3
from sqlite3 import Connection, Cursor
from typing import Any, Dict, List


class SQLiteWrapper:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.connection: Connection = sqlite3.Connection(self.db_file)
        self.connection.close()

    def open_connection(self) -> None:
        self.connection = sqlite3.Connection(self.db_file)
        self.connection.row_factory = sqlite3.Row

    def _execute(self, query: str, args: Any = None) -> Cursor:
        self.open_connection()
        if args:
            res = self.connection.cursor().execute(query, args)
        else:
            res = self.connection.cursor().execute(query)
        return res

    def insert(self, query: str, table: str, args: Any = None) -> Any:
        cursor = self._execute(query, args)
        res = cursor.execute(
            f"select * from {table} where id = ?", (cursor.lastrowid,)
        ).fetchone()
        self.connection.commit()
        self.connection.close()
        return res

    def create(self, query: str) -> None:
        self._execute(query)
        self.connection.close()

    def update(self, query: str, args: Any = None) -> Any:
        cursor = self._execute(query, args)
        res = cursor.fetchone()
        self.connection.commit()
        self.connection.close()
        return res

    def select(self, query: str, args: Any = None) -> Dict[str, Any]:
        cursor = self._execute(query, args)
        res = cursor.fetchone()
        self.connection.close()
        return res

    def select_all(
        self, query: str, args: Any = None, n: int = 0
    ) -> List[Dict[str, Any]]:
        cursor = self._execute(query, args)
        if n <= 0:
            res = cursor.fetchall()
        else:
            res = cursor.fetchmany(n)
        self.connection.close()
        return res

    # def get_connection(self) -> Connection:
    #     self.conn = sqlite3.connect(self.db_file)
    #     self.conn.row_factory = sqlite3.Row
    #     return self.conn
    #
    # def close_connection(self, connection: Connection) -> None:
    #     connection.close()
    #
    # def create_table(self, create_table_sql: str) -> None:
    #     conn = self.get_connection()
    #     conn.cursor().execute(create_table_sql)
    #     self.close_connection(conn)
    #
    # def fetch_all(
    #     self, query: str, connection: Connection, args: Optional[Any] = None
    # ) -> Any:
    #     return self._execute_cursor(
    #         query=query, connection=connection, args=args
    #     ).fetchall()
    #
    # def fetch_one(
    #     self, query: str, connection: Connection, args: Optional[Any] = None
    # ) -> Any:
    #     return self._execute_cursor(
    #         query=query, connection=connection, args=args
    #     ).fetchone()
    #
    # def execute(self, query: str, args: Any = None) -> Any:
    #     connection = self.get_connection()
    #     result = self._execute_cursor(
    #         query=query, connection=connection, args=args
    #     )
    #     connection.commit()
    #     connection.close()
    #     return result
    #
    # def _execute_cursor(
    #     self, query: str, connection: Connection, args: Optional[Any] = None
    # ) -> Any:
    #     if args:
    #         return connection.cursor().execute(query, args)
    #     return connection.cursor().execute(query)
