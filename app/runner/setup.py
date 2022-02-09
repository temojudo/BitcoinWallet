from fastapi import FastAPI


def setup() -> FastAPI:
    app = FastAPI()
    # app.include_router(receipt_api)
    # app.state.core = StoreService.create(pos=Pos(store_repository=InMemoryRepository()))

    return app
