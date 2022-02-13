from typing import List

from app.core.http.exception import ApiException
from app.core.transaction.transaction import Transaction
from app.core.wallet.balance import Balance
from app.core.wallet.wallet import Wallet
from app.infra.in_memory.storage import Storage


class InMemoryWalletRepository:
    def __init__(self, storage: Storage):
        self.storage = storage
        self.id_seq = 0

    def save(self, wallet: Wallet) -> Wallet:
        self.id_seq += 1
        wallet.id = self.id_seq
        owner = wallet.owner
        if owner in self.storage.wallets:
            self.storage.wallets[owner].append(wallet)
        else:
            self.storage.wallets[owner] = [wallet]
        return wallet

    def fetch_by_wallet_address(self, address: str) -> Wallet:
        for owner in self.storage.wallets:
            wallets = self.storage.wallets[owner]
            for wallet in wallets:
                if wallet.address == address:
                    return wallet
        raise ApiException("invalid wallet address")

    def update_balance(self, wallet_address: str, amount: float) -> Wallet:
        for owner in self.storage.wallets:
            wallets = self.storage.wallets[owner]
            for i in range(len(wallets)):
                wallet = wallets[i]
                if wallet.address == wallet_address:
                    self.storage.wallets[owner][i].balance += amount
                    return wallet
        raise ApiException("invalid wallet address")

    def get_wallet_transactions(self, address: str) -> List[Transaction]:
        result: List[Transaction] = []
        for transaction_id in self.storage.transactions:
            transaction = self.storage.transactions[transaction_id]
            if transaction.source == address or transaction.destination == address:
                result.append(transaction)
        return result
