from fastapi import APIRouter, HTTPException, Request
from bson import ObjectId
from typing import List
import yfinance as yf
from app.models import CryptoData, Customer
from app.database.mongo import get_collections
from pymongo.collection import ReturnDocument
from app.utils import authutils
from fastapi import Depends

router = APIRouter()

@router.get("/", response_model=List[CryptoData])
async def get_cryptos_data():
    collections = await get_collections()
    cryptos = await collections["crypto_history"].find().to_list(length=100)
    return cryptos

@router.post("/", response_model=CryptoData)
async def create_crypto_data(cryptodata: CryptoData, user: Customer = Depends(authutils.get_current_user)):
    collections = await get_collections()
    cryptodata_dict = cryptodata.dict(by_alias=True)
    result = await collections["crypto_history"].insert_one(cryptodata_dict)
    created_crypto = await collections["crypto_history"].find_one({"_id": result.inserted_id})
    if created_crypto is None:
        raise HTTPException(status_code=404, detail="The created crypto data was not found")
    return CryptoData(**created_crypto)
