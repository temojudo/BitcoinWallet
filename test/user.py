from test import create_facade

from app.core.user.dto import UserRegisterRequest


def test_should_create_facade() -> None:
    create_facade()


def test_create() -> None:
    service = create_facade()
    req = UserRegisterRequest("saba")
    resp = service.register_user(req)
    assert resp.username == "saba"

    # with pytest.raises(ApiException):
