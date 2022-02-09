from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class User:
    username: str
    api_key: str
    id: Optional[int] = None

    @classmethod
    def from_dao(cls, db_user: Dict[str, Any]) -> "User":
        return cls(
            id=db_user["id"], username=db_user["username"], api_key=db_user["api_key"]
        )
