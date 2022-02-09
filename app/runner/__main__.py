import uvicorn

from app.runner.asgi import app

if __name__ == "__main__":
    # import datetime as dt
    #
    # import pandas_datareader as web
    #
    # start = dt.datetime.now().date()
    # end = dt.datetime.now()
    #
    # btc_to_usd = web.DataReader("BTC-USD", "yahoo", start, end)
    #
    # print(btc_to_usd[0][0])

    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
