from fastapi import APIRouter, Depends

from app.core.facade import WalletService
from app.core.wallet.dto import GetWalletRequest, WalletCreateRequest
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


@wallet_api.get("/wallets/{address}")
def get_wallet(
    address: str, api_key: str, service: WalletService = Depends(get_service)
) -> ResponseObject:
    try:
        response = service.get_wallet(
            GetWalletRequest(api_key=api_key, address=address)
        )
        return ResponseObject.success_object(response)
    except ApiException as e:
        return ResponseObject.fail(e.message, e.status)
