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
