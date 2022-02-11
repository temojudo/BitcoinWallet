from sqlite3 import Error

from app.core.wallet.wallet import Wallet
from app.infra.http.exception import ApiException
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

    def update_balance(self, wallet: Wallet, amount: float) -> Wallet:
        query = UPDATE_WALLET_BALANCE_QUERY

        self._wrapper.update(query, (amount, wallet.id))
        return self.fetch_by_wallet_address(wallet.address)


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
                    WHERE id=?"""
