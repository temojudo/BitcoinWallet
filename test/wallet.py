from test import create_facade

from app.core.user.dto import UserRegisterRequest
from app.core.wallet.dto import WalletCreateRequest
from app.infra.factory.wallet import DefaultWalletFactory


def test_wallet_create() -> None:
    service = create_facade()
    # TODO do
    service.wallet_interactor.factory = DefaultWalletFactory()
    username = "saba"
    register_request = UserRegisterRequest(username)
    user = service.user_interactor.register(register_request)
    req = WalletCreateRequest(user.api_key)
    wallet = service.wallet_interactor.create(req)
    assert wallet.owner == user.api_key


def test_multiple_wallet() -> None:
    service = create_facade()
    username = "saba"
    register_request = UserRegisterRequest(username)
    user = service.user_interactor.register(register_request)
    req = WalletCreateRequest(user.api_key)
    wallet = service.wallet_interactor.create(req)
    wallet2 = service.wallet_interactor.create(req)
    assert wallet.owner == user.api_key
    assert wallet2.owner == user.api_key
    assert wallet.address != wallet2.address


def test_users_wallets() -> None:
    service = create_facade()
    username = "saba"
    register_request = UserRegisterRequest(username)
    user = service.user_interactor.register(register_request)
    req = WalletCreateRequest(user.api_key)
    service.wallet_interactor.create(req)
    service.wallet_interactor.create(req)
    user_with_wallets = service.user_interactor.get_by_api_key(user.api_key)
    assert len(user_with_wallets.wallets) == 2
    for wallet in user_with_wallets.wallets:
        assert wallet.owner == user.api_key


def test_wallet_address() -> None:
    service = create_facade()
    username = "saba"
    register_request = UserRegisterRequest(username)
    user = service.user_interactor.register(register_request)
    req = WalletCreateRequest(user.api_key)
    created_wallet = service.wallet_interactor.create(req)
    fetched_wallet = service.wallet_interactor.get_by_wallet_address(
        created_wallet.address
    )
    assert fetched_wallet.owner == created_wallet.owner
    assert fetched_wallet.id == created_wallet.id


def test_balance_update() -> None:
    service = create_facade()
    username = "saba"
    register_request = UserRegisterRequest(username)
    user = service.user_interactor.register(register_request)
    req = WalletCreateRequest(user.api_key)
    wallet = service.wallet_interactor.create(req)
    initial = wallet.balance.btc
    update = 0.7
    updated_wallet = service.wallet_interactor.repository.update_balance(
        wallet.address, update
    )
    assert updated_wallet.balance.btc - initial == update


def test_multiple_balance_updates() -> None:
    service = create_facade()
    username = "saba"
    register_request = UserRegisterRequest(username)
    user = service.user_interactor.register(register_request)
    req = WalletCreateRequest(user.api_key)
    wallet = service.wallet_interactor.create(req)
    repo = service.wallet_interactor.repository
    initial = wallet.balance.btc
    changed = 0.0
    repo.update_balance(wallet.address, 0.3)
    changed += 0.3
    repo.update_balance(wallet.address, 0.8)
    changed += 0.8
    updated_wallet = repo.update_balance(wallet.address, -0.6)
    changed -= 0.6
    assert updated_wallet.balance.btc == initial + changed
