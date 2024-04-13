from fastapi import APIRouter, HTTPException, Request

from bson import ObjectId
from typing import List
import yfinance as yf
from app.models import StockData,Customer
from fastapi import APIRouter, HTTPException
from ..models import Agent, PyObjectId
from ..database.mongo import get_collections
from bson import ObjectId
from pymongo.collection import ReturnDocument
from app.utils import authutils
from fastapi import APIRouter, HTTPException, Request,Depends

router = APIRouter()


@router.get("/", response_model=list[StockData])
async def get_stocksdata():
    collections = await get_collections()
    stocks = await collections["stock_history"].find().to_list(length=100)
    return stocks



@router.post("/", response_model=StockData)
async def create_stockdata(stockdata: StockData,user: Customer = Depends(authutils.get_current_user)):
    collections = await get_collections()
    stockdata_dict = stockdata.dict(by_alias=True)  
    result = await collections["stock_history"].insert_one(stockdata_dict)
    created_stock = await collections["stock_history"].find_one({"_id": result.inserted_id})
    if created_stock is None:
        raise HTTPException(status_code=404, detail="The created stock data was not found")
    return StockData(**created_stock)


# @router.get("/{ytic}", response_model=List[StockData])
# async def create_batch_items(tickers: str):
#     collections = await get_collections()
#     results = []
    
#     for ytic in tickers:
#         existing_stock = await collections["stock_history"].find_one({'Company_ticker': ytic})
#         if existing_stock:
#             results.append(StockData(**existing_stock))
#             continue

#         try:
#             comp = yf.Ticker(ytic)
#             if "longName" not in comp.info:
#                 raise HTTPException(status_code=404, detail="Yahoo Finance ticker not found")
#         except Exception as e:
#             raise HTTPException(status_code=400, detail=str(e))

#         stock_data = {
#             'Company_name': comp.info['longName'],
#             'Company_ticker': comp.info['symbol'],
#             'Closed_price': comp.info['previousClose'],
#             'Company_info': comp.info['longBusinessSummary'],
#             'Company_PE': comp.info.get('trailingPE', None),
#             'Company_cash_flow': comp.info.get('operatingCashflow', None),
#             'Company_dividend': comp.info.get('dividendRate', None)
#         }

#         result = await collections["stock_history"].insert_one(stock_data)
#         created_stock = await collections["stock_history"].find_one({"_id": result.inserted_id})
#         results.append(StockData(**created_stock))

#     return results