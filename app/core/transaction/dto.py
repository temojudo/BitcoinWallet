from dataclasses import dataclass
from typing import Any, Dict, List

from app.core.transaction.transaction import Transaction


@dataclass
class MakeTransactionRequest:
    api_key: str
    source: str
    destination: str
    amount: float


@dataclass
class TransactionResponse:
    fee: float
    amount: float
    destination: str
    source: str

    @classmethod
    def from_transaction(cls, transaction: Transaction) -> "TransactionResponse":
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
class Statistics:
    num_transactions: int
    profit: float

    @classmethod
    def from_dao(cls, db_statistics: Dict[str, Any]) -> "Statistics":
        return cls(
            num_transactions=db_statistics["num_transactions"],
            profit=db_statistics["total_fee"],
        )
