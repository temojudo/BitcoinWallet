from typing import Any

from starlette.requests import Request


def get_service(request: Request) -> Any:
    return request.app.state.core
