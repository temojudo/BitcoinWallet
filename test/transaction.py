from app.core.transaction.transaction import Transaction


def test_should_create_transaction() -> None:
    Transaction(source="src", destination="dest", amount=1, fee=0)
    # with pytest.raises(ApiException):


# def test_facade_should_save_transaction() -> None:
#     service = create_facade()
#     Transaction(source="src", destination="dest", amount=1, fee=0)
#     request = MakeTransactionRequest(
#         api_key="api", source="src", destination="dst", amount=1
#     )
#     service.make_transaction(request)
