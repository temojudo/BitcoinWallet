from fastapi import APIRouter, Depends

from app.core.facade import WalletService
from app.core.user.dto import UserRegisterRequest
from app.core.wallet.dto import WalletCreateRequest
from app.infra.fastapi.injectables import get_service
from app.infra.http.exception import ApiException
from app.infra.http.response import ResponseObject

wallet_api = APIRouter(tags=["wallet"])


@wallet_api.post("/wallets")
def create_wallet(
    request: WalletCreateRequest, service: WalletService = Depends(get_service)
) -> ResponseObject:
    try:
        response = service.create_wallet(request)
        return ResponseObject.success_object(response)
    except ApiException as e:
        return ResponseObject.fail(e.message, e.status)
