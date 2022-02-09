from fastapi import APIRouter, Depends

from app.core.facade import WalletService
from app.core.user.dto import UserRegisterRequest
from app.infra.fastapi.injectables import get_service
from app.infra.http.exception import ApiException
from app.infra.http.response import ResponseObject

user_api = APIRouter(tags=["user"])


@user_api.post("/users")
def register_user(
    request: UserRegisterRequest, service: WalletService = Depends(get_service)
) -> ResponseObject:
    try:
        response = service.register_user(request)
        return ResponseObject.success_object(response)
    except ApiException as e:
        return ResponseObject.fail(e.message, e.status)
