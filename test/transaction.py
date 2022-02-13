from test import create_facade

import pytest

from app.core import ADMIN_API_KEY
from app.core.http.exception import ApiException
from app.core.transaction.dto import GetTransactionsRequest, MakeTransactionRequest
from app.core.transaction.transaction import Transaction
from app.core.user.dto import UserRegisterRequest
from app.core.wallet.dto import WalletCreateRequest


def test_should_create_transaction() -> None:
    Transaction(source="src", destination="dest", amount=1, fee=0)


def test_should_not_save_transaction() -> None:
    service = create_facade()
    Transaction(source="src", destination="dest", amount=1, fee=0)
    request = MakeTransactionRequest(
        api_key="api", source="src", destination="dst", amount=1
    )
    with pytest.raises(ApiException):
        service.make_transaction(request)


def test_should_not_make_transaction_with_insufficient_balance() -> None:
    service = create_facade()
    user_request = UserRegisterRequest("saba")
    user_response = service.register_user(user_request)
    wallet_request = WalletCreateRequest(user_response.api_key)
    wallet_response_a = service.create_wallet(wallet_request)
    wallet_response_b = service.create_wallet(wallet_request)
    request = MakeTransactionRequest(
        api_key=user_response.api_key,
        source=wallet_response_a.address,
        destination=wallet_response_b.address,
        amount=10,
    )
    with pytest.raises(ApiException):
        service.make_transaction(request)


def test_should_save_transaction() -> None:
    service = create_facade()
    user_request = UserRegisterRequest("saba")
    user_response = service.register_user(user_request)
    wallet_request = WalletCreateRequest(user_response.api_key)
    wallet_response_a = service.create_wallet(wallet_request)
    wallet_response_b = service.create_wallet(wallet_request)
    request = MakeTransactionRequest(
        api_key=user_response.api_key,
        source=wallet_response_a.address,
        destination=wallet_response_b.address,
        amount=1,
    )
    service.make_transaction(request)
    get_transactions_request = GetTransactionsRequest(user_response.api_key)
    transactions = service.get_transactions(get_transactions_request)
    assert len(transactions) == 1
    assert transactions[0].source == wallet_response_a.address
    assert transactions[0].destination == wallet_response_b.address
    assert transactions[0].fee == 0
    assert transactions[0].amount == 1


def test_should_save_multiple_transactions() -> None:
    service = create_facade()
    user_request = UserRegisterRequest("saba")
    user_response = service.register_user(user_request)
    wallet_request = WalletCreateRequest(user_response.api_key)
    wallet_response_a = service.create_wallet(wallet_request)
    wallet_response_b = service.create_wallet(wallet_request)
    request = MakeTransactionRequest(
        api_key=user_response.api_key,
        source=wallet_response_a.address,
        destination=wallet_response_b.address,
        amount=0.6,
    )
    service.make_transaction(request)
    request = MakeTransactionRequest(
        api_key=user_response.api_key,
        source=wallet_response_a.address,
        destination=wallet_response_b.address,
        amount=0.4,
    )
    service.make_transaction(request)
    get_transactions_request = GetTransactionsRequest(user_response.api_key)
    transactions = service.get_transactions(get_transactions_request)
    assert len(transactions) == 2
    assert transactions[0].source == wallet_response_a.address
    assert transactions[0].destination == wallet_response_b.address
    assert transactions[0].fee == 0
    assert transactions[0].amount == 0.6
    assert transactions[1].source == wallet_response_a.address
    assert transactions[1].destination == wallet_response_b.address
    assert transactions[1].fee == 0
    assert transactions[1].amount == 0.4


def test_should_not_get_statistics_for_non_admin() -> None:
    service = create_facade()
    with pytest.raises(ApiException):
        service.get_statistics("non-admin-api-key")


def test_should_get_empty_statistics() -> None:
    service = create_facade()
    statistics = service.get_statistics(ADMIN_API_KEY)
    assert statistics.num_transactions == 0
    assert statistics.profit == 0


def test_should_get_statistics_single_non_profit() -> None:
    service = create_facade()
    user_request = UserRegisterRequest("test")
    user_response = service.register_user(user_request)
    wallet_request = WalletCreateRequest(user_response.api_key)
    wallet_response_a = service.create_wallet(wallet_request)
    wallet_response_b = service.create_wallet(wallet_request)
    request = MakeTransactionRequest(
        api_key=user_response.api_key,
        source=wallet_response_a.address,
        destination=wallet_response_b.address,
        amount=1,
    )
    service.make_transaction(request)
    statistics = service.get_statistics(ADMIN_API_KEY)
    assert statistics.num_transactions == 1
    assert statistics.profit == 0.0


def test_should_get_statistics_single_with_profit() -> None:
    service = create_facade()
    user_request_a = UserRegisterRequest("user1")
    user_response_a = service.register_user(user_request_a)
    user_request_b = UserRegisterRequest("user2")
    user_response_b = service.register_user(user_request_b)
    wallet_request_a = WalletCreateRequest(user_response_a.api_key)
    wallet_request_b = WalletCreateRequest(user_response_b.api_key)
    wallet_response_a = service.create_wallet(wallet_request_a)
    wallet_response_b = service.create_wallet(wallet_request_b)
    request = MakeTransactionRequest(
        api_key=user_response_a.api_key,
        source=wallet_response_a.address,
        destination=wallet_response_b.address,
        amount=1,
    )
    service.make_transaction(request)
    statistics = service.get_statistics(ADMIN_API_KEY)
    assert statistics.num_transactions == 1
    assert statistics.profit == 0.015


def test_should_get_statistics_multi() -> None:
    service = create_facade()
    user_request = UserRegisterRequest("test")
    user_response = service.register_user(user_request)
    wallet_request = WalletCreateRequest(user_response.api_key)
    wallet_response_a = service.create_wallet(wallet_request)
    wallet_response_b = service.create_wallet(wallet_request)
    request = MakeTransactionRequest(
        api_key=user_response.api_key,
        source=wallet_response_a.address,
        destination=wallet_response_b.address,
        amount=0.6,
    )
    service.make_transaction(request)
    request = MakeTransactionRequest(
        api_key=user_response.api_key,
        source=wallet_response_a.address,
        destination=wallet_response_b.address,
        amount=0.4,
    )
    service.make_transaction(request)
    statistics = service.get_statistics(ADMIN_API_KEY)
    assert statistics.num_transactions == 2
    assert statistics.profit == 0.0
