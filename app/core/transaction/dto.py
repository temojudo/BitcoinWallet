from dataclasses import dataclass
from typing import List

from app.core.transaction.transaction import Transaction


@dataclass
class MakeTransactionRequest:
    api_key: str
    source: str
    destination: str
    amount: float


@dataclass
class MakeTransactionResponse:
    fee: float
    amount: float
    destination: str
    source: str

    @classmethod
    def from_transaction(cls, transaction: Transaction) -> "MakeTransactionResponse":
        return cls(
            fee=transaction.fee,
            amount=transaction.amount,
            destination=transaction.destination,
            source=transaction.source,
        )


@dataclass
class GetTransactionsRequest:
    api_key: str


@dataclass
class TransactionBaseModel:
    source: str
    destination: str
    amount: float
    fee: float


@dataclass
class GetTransactionsResponse:
    transactions: List[TransactionBaseModel]

    @classmethod
    def from_transactions(
        cls, transactions: List[Transaction]
    ) -> "GetTransactionsResponse":
        transaction_models = [
            TransactionBaseModel(
                source=transaction.source,
                destination=transaction.destination,
                amount=transaction.amount,
                fee=transaction.fee,
            )
            for transaction in transactions
        ]
        return cls(transactions=transaction_models)
