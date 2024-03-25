from yahooquery import Ticker

async def get_stock_info(ticker_symbol):
    ticker = Ticker(ticker_symbol)
    stock_info = ticker.summary_detail[ticker_symbol]
    return stock_info

async def get_stock_history(ticker_symbol):
    ticker = Ticker(ticker_symbol)
    history = ticker.history(period="max")
    history.reset_index(inplace=True)
    history_data = history.to_dict("records")
    return history_data