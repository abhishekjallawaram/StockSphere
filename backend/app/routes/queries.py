from fastapi import APIRouter, HTTPException, Request,Depends, Query
from pydantic import BaseModel, EmailStr
from fastapi.security import OAuth2PasswordRequestForm
from bson import ObjectId
from typing import List,Optional,Any
import yfinance as yf
from app.models import Customer
from app.routes.schemas import CustomerRequenst,CustomerResponse,UserAuth,TokenSchema
from fastapi import APIRouter, HTTPException
from ..database.mongo import get_collections
from bson import ObjectId
from pymongo.collection import ReturnDocument
from fastapi import APIRouter, HTTPException, status
from app.utils import authutils
from fastapi import APIRouter, HTTPException, Request,Depends
from app.routes.schemas import CustomerInfo, AgentInfo, CustomerTransactionInfo
from app.database.mongo import get_top_customers, get_top_agents, get_customers_most_transactions


router = APIRouter()

@router.get("/query1-output/", response_model=list[CustomerInfo])
async def fetch_customer_data(limit: int = Query(5, title="Limit", description="Number of results to return", ge=5, le=20)):
    result = await get_top_customers(limit)
    return result

@router.get("/query2-output/", response_model=list[AgentInfo])
async def fetch_top_agents(limit: int = Query(5, title="Limit", description="Number of results to return", ge=5, le=20)):
    try:
        agents = await get_top_agents(limit)
        return agents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/customers/most-transactions/", response_model=list[CustomerTransactionInfo])
async def fetch_customers_most_transactions(limit: int = Query(5, title="Limit", description="Number of results to return", ge=5, le=20)):
    try:
        customers = await get_customers_most_transactions(limit)
        return customers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))