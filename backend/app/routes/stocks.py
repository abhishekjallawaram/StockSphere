from fastapi import APIRouter, HTTPException, Request

from bson import ObjectId
from typing import List
import yfinance as yf
from app.models import Stock,CreateStockRequest
from fastapi import APIRouter, HTTPException
from ..models import Agent, PyObjectId
from ..database.mongo import get_collections
from bson import ObjectId
from pymongo.collection import ReturnDocument

router = APIRouter()


#get all the stocks
@router.get("/", response_model=list[Stock])
async def get_stocks():
    collections = await get_collections()
    stocks = await collections["stocks"].find().to_list(length=100)
    return stocks




@router.post("/", response_model=Stock)
async def create_stock(stock: CreateStockRequest):
    collections = await get_collections()

    
    max_id_doc = await collections["stocks"].find_one(sort=[("stock_id", -1)])
    max_id = max_id_doc['stock_id'] + 1 if max_id_doc and 'stock_id' in max_id_doc else 1


    stock_data = stock.dict(by_alias=True)
    stock_data["stock_id"] = max_id


    result = await collections["stocks"].insert_one(stock_data)
    created_stock = await collections["stocks"].find_one({"_id": result.inserted_id})
    return created_stock

#get stock by stockid
@router.get("/{stockid}", response_model=Stock)
async def read_stock_byid(stockid: int):
    collections = await get_collections()
    item = await collections["stocks"].find_one({"stock_id": stockid})
    if item:
        return Stock(**item)
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("/{ytic}", response_model=Stock)
async def create_item(ytic: str):
    collections = await get_collections()
    existing_stock = await collections["stocks"].find_one({'Company_ticker': ytic})
    if existing_stock:
        return Stock(**existing_stock)
    
    try:
        comp = yf.Ticker(ytic)
        if "longName" not in comp.info:
            raise HTTPException(status_code=404, detail="Yahoo Finance ticker not found")
    except Exception as e: 
        raise HTTPException(status_code=400, detail=str(e))
    body = {
        'Company_name': comp.info['longName'],
        'Company_ticker': comp.info['symbol'],
        'Closed_price': comp.info['previousClose'],
        'Company_info': comp.info['longBusinessSummary'],
        'Company_PE': comp.info.get('trailingPE', None), 
        'Company_cash_flow': comp.info.get('operatingCashflow', None),
        'Company_dividend': comp.info.get('dividendRate', None)
    }
    
    stock_data = CreateStockRequest(
                    Company_name=comp.info['longName'],
                    Company_ticker=comp.info['symbol'],
                    Closed_price=comp.info['previousClose'],
                    Company_info=comp.info['longBusinessSummary'],
                    Company_PE=comp.info.get('trailingPE', None),
                    Company_cash_flow=comp.info.get('operatingCashflow', None),
                    Company_dividend=comp.info.get('dividendRate', None)
                   
                )
                
    result = await create_stock(stock=stock_data)
    created_stock = Stock(**stock_data, id=result.inserted_id)
    return created_stock


#update Stock
@router.put("/{stockid}", response_model=Stock)
async def update_stock(stockid: int, update_data: CreateStockRequest):
    collections = await get_collections()
    updated_stock = await collections["stocks"].find_one_and_update(
        {"stock_id": stockid},
        {"$set": update_data.dict(by_alias=True)},
        return_document=ReturnDocument.AFTER
    )

    if updated_stock:
        return Stock(**updated_stock)
    else:
        raise HTTPException(status_code=404, detail="Stock not found")
    

@router.put("/{ytic}", response_model=Stock)
async def update_stock_by_ticker(ytic: str, update_data: CreateStockRequest):
    collections = await get_collections()
    updated_stock = await collections["stocks"].find_one_and_update(
        {"Company_ticker": ytic},
        {"$set": update_data.dict(by_alias=True)},
        return_document=ReturnDocument.AFTER
    )

    if updated_stock:
        return Stock(**updated_stock)
    else:
        raise HTTPException(status_code=404, detail="Stock with given ticker not found")


#delete Stock 
@router.delete("/{stockid}", response_model=dict)
async def delete_stock(stockid: int):
    collections = await get_collections()
    delete_result = await collections["stocks"].delete_one({"stock_id": stockid})

    if delete_result.deleted_count == 1:
        return {"message": "Stock deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    

@router.delete("/{ytic}", response_model=dict)
async def delete_stock_by_ticker(ytic: str):
    collections = await get_collections()
    delete_result = await collections["stocks"].delete_one({"Company_ticker": ytic})

    if delete_result.deleted_count == 1:
        return {"message": "Stock with ticker '{}' deleted successfully".format(ytic)}
    else:
        raise HTTPException(status_code=404, detail="Stock with given ticker not found")
