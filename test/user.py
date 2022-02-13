from test import create_facade

import pytest

from app.core.http.exception import ApiException
from app.core.user.dto import UserRegisterRequest, UserRegisterResponse
from app.core.user.user import User


def test_should_create_facade() -> None:
    create_facade()


def test_register() -> None:
    service = create_facade()
    username = "saba"
    req = UserRegisterRequest(username)
    resp = service.register_user(req)
    assert resp.username == username


def test_get_existing_user() -> None:
    service = create_facade()
    username = "saba"
    req = UserRegisterRequest(username)
    resp = service.register_user(req)
    user = service.user_interactor.get_by_api_key(resp.api_key)
    assert user.username == username
    assert user.id == 0


def test_get_non_existent_user() -> None:
    service = create_facade()
    username = "saba"
    req = UserRegisterRequest(username)
    resp = service.register_user(req)
    with pytest.raises(ApiException):
        service.user_interactor.get_by_api_key(f"{resp.api_key}asd")


def test_multiple_users() -> None:
    service = create_facade()
    usernames = ["nino", "saba", "xuco", "leviii", "saba ogond magari"]

    api_keys = []
    for username in usernames:
        req = UserRegisterRequest(username)
        resp = service.register_user(req)
        api_keys.append(resp.api_key)

    for i, key in enumerate(api_keys):
        user = service.user_interactor.get_by_api_key(key)
        assert user.id == i
        assert user.username == usernames[i]


def test_user_creation() -> None:
    tid, key, username = 0, "rand_key_ye_ye", "saba magaria"
    db_user = {"id": tid, "api_key": key, "username": username}

    user = User.from_dao(db_user)
    assert user.id == tid
    assert user.username == username
    assert user.api_key == key


def test_user_response_creation() -> None:
    key, username = "rand_key_ye_ye", "saba magaria"
    user = User(username, key)
    resp = UserRegisterResponse.from_user(user)

    assert resp.username == username
    assert resp.api_key == key
