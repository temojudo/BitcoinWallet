from sqlite3 import Error
from typing import List

from app.core.http.exception import ApiException
from app.core.transaction.transaction import Transaction
from app.core.wallet.wallet import Wallet
from app.infra.sqlite.db_wrapper import SQLiteWrapper


class SQLiteWalletRepository:
    def __init__(self, db_uri: str):
        self.db_uri = db_uri
        self._wrapper = SQLiteWrapper(db_uri)
        try:
            self._wrapper.create(CREATE_WALLET_TABLE_QUERY)
        except Error as e:
            raise ApiException(f"Couldn't connect to database\nstacktrace: {e}")

    def save(self, wallet: Wallet) -> Wallet:
        query = INSERT_WALLET_QUERY

        if wallet.id != -1:
            raise ApiException("Given already created wallet")

        db_wallet = self._wrapper.insert(
            query,
            "wallets",
            (wallet.owner, wallet.address, wallet.balance.btc),
        )

        return Wallet.from_dao(db_wallet)

    def fetch_by_wallet_address(self, address: str) -> Wallet:
        query = FETCH_WALLET_BY_ADDRESS_QUERY

        db_wallet = self._wrapper.select(query, (address,))

        return Wallet.from_dao(db_wallet)

    def update_balance(self, wallet_address: str, amount: float) -> Wallet:
        query = UPDATE_WALLET_BALANCE_QUERY

        self._wrapper.update(query, (amount, wallet_address))
        return self.fetch_by_wallet_address(wallet_address)

    def get_wallet_transactions(self, address: str) -> List[Transaction]:
        query = FETCH_BY_WALLET_ADDRESS_QUERY

        db_transactions = self._wrapper.select_all(query, (address, address))

        if not db_transactions:
            raise ApiException("Wrong wallet address", 406)

        return [Transaction.from_dao(transaction) for transaction in db_transactions]


CREATE_WALLET_TABLE_QUERY = """
                CREATE TABLE IF NOT EXISTS wallets (
                    id integer PRIMARY KEY,
                    owner text NOT NULL,
                    address text NOT NULL UNIQUE,
                    btc float NOT NULL default 0
                );"""

INSERT_WALLET_QUERY = """ INSERT INTO wallets(owner, address, btc)
                            VALUES (?,?,?)"""

FETCH_WALLET_BY_ADDRESS_QUERY = """ 
                SELECT * FROM wallets
                WHERE address=?"""

UPDATE_WALLET_BALANCE_QUERY = """UPDATE wallets
                    SET btc=btc+?
                    WHERE address=?"""


FETCH_BY_WALLET_ADDRESS_QUERY = """ SELECT * FROM transactions
                    WHERE destination_address LIKE ? OR source_address LIKE ?"""
