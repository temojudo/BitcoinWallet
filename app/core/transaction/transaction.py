from typing import Any, Dict


class Transaction:
    def __init__(self, source: str, destination: str, amount: float, fee: float):
        self.id: int = -1
        self.source = source
        self.destination = destination
        self.amount = amount
        self.fee = fee

    @classmethod
    def from_dao(cls, db_transaction: Dict[str, Any]) -> "Transaction":
        transaction = cls(
            source=db_transaction["source_address"],
            destination=db_transaction["destination_address"],
            amount=db_transaction["amount"],
            fee=db_transaction["fee"],
        )
        transaction.id = db_transaction["id"]
        return transaction
