from dataclasses import dataclass

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
