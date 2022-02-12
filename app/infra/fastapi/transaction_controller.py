from fastapi import APIRouter, Depends

from app.core.facade import WalletService
from app.core.transaction.dto import GetTransactionsRequest, MakeTransactionRequest
from app.infra.fastapi.injectables import get_service
from app.infra.http.exception import ApiException
from app.infra.http.response import ResponseObject

transaction_api = APIRouter(tags=["transaction"])


@transaction_api.post("/transactions")
def make_transaction(
    request: MakeTransactionRequest, service: WalletService = Depends(get_service)
) -> ResponseObject:
    try:
        response = service.make_transaction(request)
        return ResponseObject.success_object(response)
    except ApiException as e:
        return ResponseObject.fail(e.message, e.status)


@transaction_api.get("/transactions/{api_key}")
def get_transactions(
    api_key: str, service: WalletService = Depends(get_service)
) -> ResponseObject:
    try:
        response = service.get_transactions(GetTransactionsRequest(api_key))
        return ResponseObject.success_object(response)
    except ApiException as e:
        return ResponseObject.fail(e.message, e.status)
