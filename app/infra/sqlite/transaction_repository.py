from sqlite3 import Error
from typing import List

from app.core.http.exception import ApiException
from app.core.transaction.dto import Statistics
from app.core.transaction.transaction import Transaction
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

    def fetch_by_api_key(self, api_key: str) -> List[Transaction]:
        query = FETCH_BY_API_KEY_QUERY

        db_transactions = self._wrapper.select_all(query, (api_key,))

        return [Transaction.from_dao(transaction) for transaction in db_transactions]

    def query_statistics(self) -> Statistics:
        query = TRANSACTION_STATISTICS_QUERY
        db_statistics = self._wrapper.select(query)
        return Statistics.from_dao(db_statistics)


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

FETCH_BY_API_KEY_QUERY = """ 
                SELECT transactions.id, source_address, destination_address, amount, fee FROM transactions
                JOIN wallets ON (transactions.source_address=wallets.address OR transactions.destination_address=wallets.address)
                WHERE wallets.owner=?
                GROUP BY transactions.id
                """

TRANSACTION_STATISTICS_QUERY = """
SELECT count(*) as num_transactions, sum(fee) as total_fee from transactions
"""
