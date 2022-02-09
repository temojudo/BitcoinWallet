from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable


class ResponseType(int, Enum):
    EMPTY = 1
    OBJECT = 2
    LIST = 3
    FAIL = 4


@dataclass
class ResponseObject:
    data: Any
    type: ResponseType
    code: int = 200

    @classmethod
    def success(cls) -> "ResponseObject":
        return ResponseObject(data=None, type=ResponseType.EMPTY)

    @classmethod
    def success_object(cls, data: Any) -> "ResponseObject":
        return ResponseObject(data=data, type=ResponseType.OBJECT)

    @classmethod
    def success_list(cls, data: Iterable[Any]) -> "ResponseObject":
        return ResponseObject(data=data, type=ResponseType.LIST)

    @classmethod
    def fail(cls, message: str, code: int = 500) -> "ResponseObject":
        return ResponseObject(data=message, type=ResponseType.FAIL, code=code)
