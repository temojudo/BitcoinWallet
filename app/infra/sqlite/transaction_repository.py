from sqlite3 import Error

from app.core.transaction.transaction import Transaction
from app.infra.http.exception import ApiException
from app.infra.sqlite.db_wrapper import SQLiteWrapper


class SQLiteTransactionRepository:
    def __init__(self, db_uri: str):
        self.db_uri = db_uri
        self._wrapper = SQLiteWrapper(db_uri)
        try:
            self._wrapper.create(CREATE_TRANSACTION_TABLE_QUERY)
        except Error as e:
            raise ApiException(f"couldn't connect to database\nstacktrace: {e}")

    def save(self, transaction: Transaction) -> Transaction:
        query = INSERT_TRANSACTION_QUERY

        db_transaction = self._wrapper.insert(
            query,
            "transactions",
            (
                transaction.source,
                transaction.destination,
                transaction.amount,
                transaction.fee,
            ),
        )
        return Transaction.from_dao(db_transaction)


CREATE_TRANSACTION_TABLE_QUERY = """
                CREATE TABLE IF NOT EXISTS transactions (
                    id integer PRIMARY KEY,
                    source_address text NOT NULL,
                    destination_address text NOT NULL,
                    amount float NOT NULL,
                    fee float NOT NULL
                );"""


INSERT_TRANSACTION_QUERY = """ INSERT INTO transactions(source_address, destination_address, amount, fee)
                            VALUES (?,?,?,?)"""