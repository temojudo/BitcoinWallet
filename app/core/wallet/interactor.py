from dataclasses import dataclass

from app.core.transaction.transaction import Transaction
from app.core.user.interactor import UserInteractor
from app.core.wallet.currency_converter_strategy import (
    CurrencyConverterName,
    ICurrencyConverterStrategy,
)
from app.core.wallet.dto import GetWalletRequest, WalletCreateRequest
from app.core.wallet.factory import WalletFactory
from app.core.wallet.repository import IWalletRepository
from app.core.wallet.wallet import Wallet
from app.infra.http.exception import ApiException


@dataclass
class WalletInteractor:
    repository: IWalletRepository
    user_interactor: UserInteractor
    factory: WalletFactory
    currency_converter_strategy: ICurrencyConverterStrategy

    def create(self, wallet_request: WalletCreateRequest) -> Wallet:
        user = self.user_interactor.get_by_api_key(wallet_request.api_key)

        wallet = self.factory.create(user)
        self.repository.save(wallet)

        balance_usd = self.currency_converter_strategy.convert_currency(
            CurrencyConverterName.BTC_TO_USD, wallet.balance.btc
        )

        wallet.set_converted_currency(CurrencyConverterName.BTC_TO_USD, balance_usd)
        return wallet

    def make_transaction(self, transaction: Transaction) -> None:
        self.repository.update_balance(
            transaction.source, -(transaction.amount + transaction.fee)
        )
        self.repository.update_balance(transaction.destination, transaction.amount)

    def get_by_wallet_address(self, wallet_address: str) -> Wallet:
        return self.repository.fetch_by_wallet_address(wallet_address)

    def get(self, wallet_request: GetWalletRequest) -> Wallet:
        wallet = self.get_by_wallet_address(wallet_request.address)

        if wallet.owner != wallet_request.api_key:
            raise ApiException("Wallet address and api_key mismatch", status=404)

        balance_usd = self.currency_converter_strategy.convert_currency(
            CurrencyConverterName.BTC_TO_USD, wallet.balance.btc
        )

        wallet.set_converted_currency(CurrencyConverterName.BTC_TO_USD, balance_usd)
        return wallet
