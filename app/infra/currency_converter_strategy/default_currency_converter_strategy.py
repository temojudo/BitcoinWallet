from forex_python.bitcoin import BtcConverter

from app.core.wallet.currency_converter_strategy import CurrencyConverterName


class DefaultConverterStrategy:
    @classmethod
    def convert_currency(cls, name: CurrencyConverterName, amount: float) -> float:
        if CurrencyConverterName.BTC_TO_USD == name:
            converter_multiplier = BtcConverter().get_latest_price("USD")
            return float(converter_multiplier) * amount
        else:
            return -1  # Not supported
