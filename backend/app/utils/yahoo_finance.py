from fastapi import FastAPI
import yfinance as yf
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from bson import ObjectId
import pandas as pd
from ..models import CreateStockRequest
from ..routes.stocks import create_stock

app = FastAPI()

MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
database = client["stocksphere"]
stocks_collection = database["stocks"]
stock_history_collection = database["stock_history"]

ticker_symbols = [
    'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'BRK-B', 'JNJ', 'V', 'PG', 'JPM',
    'TSLA', 'NVDA', 'DIS', 'NFLX', 'PFE', 'KO', 'NKE', 'XOM', 'CVX', 'CSCO',
    'INTC', 'WMT', 'T', 'VZ', 'UNH', 'HD', 'MCD', 'BA', 'MMM', 'CAT',
    'GS', 'IBM', 'MRK', 'GE', 'F', 'GM', 'ADBE', 'CRM', 'ORCL', 'ABT',
    'BAC', 'C', 'GILD', 'LLY', 'MDT', 'AMGN', 'MO', 'PEP', 'TMO', 'DHR'
]

async def fetch_and_update_stock_data():
    for symbol in ticker_symbols:
        try:
            stock = yf.Ticker(symbol)
            info = stock.info

            if await stocks_collection.count_documents({'Company_ticker': info['symbol']}) == 0:
                max_id_doc = await stocks_collection.find_one(sort=[("stock_id", -1)])
                max_id = max_id_doc['stock_id'] if max_id_doc else 0
                stock_data = CreateStockRequest(
                    # stock_id=max_id + 1,
                    Company_name=info['longName'],
                    Company_ticker=info['symbol'],
                    Closed_price=info['previousClose'],
                    Company_info=info['longBusinessSummary'],
                    Company_PE=info.get('trailingPE', None),
                    Company_cash_flow=info.get('operatingCashflow', None),
                    Company_dividend=info.get('dividendRate', None)
                    # Note: You need to handle 'Company_currency' and 'stock_id' as well if they're required
                )
                await create_stock(stock=stock_data)
        except Exception as e:
            print(f"Error updating stock {symbol}: {e}")

from datetime import datetime, timedelta
import pandas as pd

async def fetch_and_store_historical_data():
    for symbol in ticker_symbols:
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="7d", interval="5m")

            if not hist.empty:
                hist.reset_index(inplace=True)
                records = hist.to_dict('records')
                for record in records:
                    record['Company_ticker'] = symbol
                    record['Date'] = datetime.combine(record['Datetime'].date(), datetime.min.time())
                    record['Time'] = record['Datetime'].time().strftime('%H:%M:%S')
                    del record['Datetime'] 


                await stock_history_collection.insert_many(records)
        except Exception as e:
            print(f"Error updating intraday data for {symbol}: {e}")



# from yahooquery import Ticker

# async def get_stock_info(ticker_symbol):
#     ticker = Ticker(ticker_symbol)
#     stock_info = ticker.summary_detail[ticker_symbol]
#     return stock_info

# async def get_stock_history(ticker_symbol):
#     ticker = Ticker(ticker_symbol)
#     history = ticker.history(period="max")
#     history.reset_index(inplace=True)
#     history_data = history.to_dict("records")
#     return history_data