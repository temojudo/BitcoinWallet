from dataclasses import dataclass


@dataclass
class ApiException(RuntimeError):
    message: str
    status: int = 500
