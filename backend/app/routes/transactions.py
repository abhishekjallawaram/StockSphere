from fastapi import APIRouter, HTTPException, Request

from typing import List, Optional
# import yfinance as yf
from fastapi import APIRouter, Depends, Query
from datetime import datetime
from app.models import Transaction,Customer,Stock
from app.routes.schemas import TransactionRequest,Cstock
from fastapi import APIRouter, HTTPException
from app.database.mongo import get_collections
from app.utils import authutils
from fastapi import APIRouter, HTTPException, Request,Depends
from pymongo.collection import ReturnDocument


router = APIRouter()

@router.get("/", response_model=list[Transaction])
async def get_stocks( user: Customer = Depends(authutils.get_current_admin)):
    userid=user.customer_id
    collections = await get_collections()
    transaction_data = await collections["transactions"].find({"customer_id": userid}).to_list(length=100)
    
    return transaction_data



@router.get("/customer-stocks", response_model=List[Cstock])
async def get_customer_stocks(user: Customer = Depends(authutils.get_current_user)):
    collections = await get_collections()
    transactions = await collections["transactions"].find({"customer_id": user.customer_id}).to_list(length=None)

    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found for the user")

    customer_stocks = [
        Cstock(
            stock_ticket=transaction["ticket"],
            each_cost=transaction["each_cost"],
            volume=transaction["volume"]
        )
        for transaction in transactions
    ]
    return customer_stocks

@router.get("/", response_model=list[Transaction])
async def get_stocks(user: Customer = Depends(authutils.get_current_admin)):
    userid=user.customer_id
    collections = await get_collections()
    transaction_data = await collections["transactions"].find({"customer_id": userid}).to_list(length=100)
    
    return transaction_data


@router.get("/{transcationid}", response_model=Transaction)
async def read_transaction_byid(transcationid: int, user: Customer = Depends(authutils.get_current_admin)):
    collections = await get_collections()
    item = await collections["transactions"].find_one({"transaction_id": transcationid})
    if item:
        return Transaction(**item)
    raise HTTPException(status_code=404, detail="Item not found")





@router.post("/", response_model=Transaction)
async def create_stock(trancation: TransactionRequest, user: Customer = Depends(authutils.get_current_user)):
    collections = await get_collections()

    max_id_doc = await collections["transactions"].find_one(sort=[("transaction_id", -1)])
    max_id = max_id_doc['transaction_id'] + 1 if max_id_doc and 'transaction_id' in max_id_doc else 1

    transaction_data = trancation.dict(by_alias=True)
    transaction_data["transaction_id"] = max_id
    transaction_data["customer_id"] = user.customer_id  
    transaction_data["date"] = datetime.now()
    
      
    result = await collections["transactions"].insert_one(transaction_data)
    created_transaction = await collections["transactions"].find_one({"_id": result.inserted_id})
    return created_transaction


@router.get("/[transactions]", response_model=List[Transaction]) 
async def get_transactions(user: Customer = Depends(authutils.get_current_admin),
    customer_id: Optional[int] = Query(None), 
    stock_id: Optional[int] = Query(None),
    action: Optional[str] = Query(None),
    ticket: Optional[str] = Query(None),
    date: Optional[datetime] = None 
):
    collections = await get_collections()

    query = {}
    if customer_id is not None:
        query['customer_id'] = customer_id
    if stock_id is not None:
        query['stock_id'] = stock_id
    if action is not None:
        query['action'] = action
    if ticket is not None:
        query['ticket'] = ticket
    if date is not None: 
        query['date'] = {'$gte': date} 

    transactions = await collections["transactions"].find(query).to_list(length=100)
    return transactions







@router.put("/{transcationid}", response_model=Transaction)
async def update_transaction(transcationid: int, update_data: TransactionRequest,user: Customer = Depends(authutils.get_current_admin)):
    collections = await get_collections()
    updated_TRANSACTION = await collections["transactions"].find_one_and_update(
        {"stock_id": transcationid},
        {"$set": update_data.dict(by_alias=True)},
        return_document=ReturnDocument.AFTER
    )
    if updated_TRANSACTION:
        return Transaction(**updated_TRANSACTION)
    else:
        raise HTTPException(status_code=404, detail="Stock not found")
    






@router.delete("/{transcationid}", response_model=dict)
async def delete_stock(transcationid: int,user: Customer = Depends(authutils.get_current_admin)):
    collections = await get_collections()
    delete_result = await collections["transactions"].delete_one({"transaction_id": transcationid})

    if delete_result.deleted_count == 1:
        return {"message": "Stock deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Stock not found")


