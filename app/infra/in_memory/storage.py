from dataclasses import dataclass, field
from typing import Dict, List

from app.core.transaction.transaction import Transaction
from app.core.user.user import User
from app.core.wallet.wallet import Wallet


@dataclass
class Storage:
    users: Dict[str, User] = field(default_factory=dict)
    wallets: Dict[str, List[Wallet]] = field(default_factory=dict)
    transactions: Dict[str, Transaction] = field(default_factory=dict)
