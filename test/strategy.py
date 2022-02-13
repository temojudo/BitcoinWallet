from app.core.wallet.balance import Balance
from app.core.wallet.currency_converter_strategy import CurrencyConverterName
from app.core.wallet.wallet import Wallet
from app.infra.currency_converter_strategy.default_currency_converter_strategy import (
    DefaultConverterStrategy,
)
from app.infra.fee_calculation_strategies.default_fee_calculation_strategy import (
    DefaultFeeCalculationStrategy,
)


def test_should_create_fee_calculation_strategy() -> None:
    DefaultFeeCalculationStrategy()


def test_fee_calculation_strategy_same_owner() -> None:
    strategy = DefaultFeeCalculationStrategy()
    owner = "test_owner"
    result = strategy.calculate_fee(
        Wallet(address="", owner=owner, balance=Balance(0.0)),
        Wallet(address="", owner=owner, balance=Balance(0.0)),
    )
    assert result == 0


def test_fee_calculation_strategy_different_owner() -> None:
    strategy = DefaultFeeCalculationStrategy()
    owner = "test_owner"
    result = strategy.calculate_fee(
        Wallet(address="", owner=owner + "1", balance=Balance(0.0)),
        Wallet(address="", owner=owner + "2", balance=Balance(0.0)),
    )
    assert result != 0
    assert result == 0.015


def test_should_create_converter_strategy() -> None:
    DefaultConverterStrategy()


def test_converter_strategy_should_fetch_data() -> None:
    strategy = DefaultConverterStrategy()
    result = strategy.convert_currency(CurrencyConverterName.BTC_TO_USD, 3.0)
    assert result != -1


def test_converter_strategy_should_fetch_consistent_data() -> None:
    strategy = DefaultConverterStrategy()
    result = strategy.convert_currency(CurrencyConverterName.BTC_TO_USD, 1.0)
    result_x_two = strategy.convert_currency(CurrencyConverterName.BTC_TO_USD, 1.0 * 2)
    assert result * 2 == result_x_two
