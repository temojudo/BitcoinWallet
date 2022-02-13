import uuid

ADMIN_API_KEY = "50cc293c-6b9e-41dc-ad74-47d340264068"


class UUIDAdapter:
    @classmethod
    def generate_api_key(cls) -> str:
        return str(uuid.uuid4())

    @classmethod
    def generate_address(cls) -> str:
        return str(uuid.uuid4())
