from enum import Enum
from typing import Protocol


class CurrencyConverterName(Enum):
    BTC_TO_USD = 1


class ICurrencyConverterStrategy(Protocol):
    def convert_currency(self, name: CurrencyConverterName, amount: float) -> float:
        pass
