from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends
import pymongo
from pymongo import mongo_client

class MongoDB:
    client = None

    @classmethod
    def get_client(cls):
        if cls.client is None:
            cls.client = AsyncIOMotorClient("mongodb://localhost:27017")
        return cls.client

async def get_database():
    client = MongoDB.get_client()
    return client.stocksphere

async def get_collections():
    db = await get_database()
    collections = {
        "agents": db.agents,
        "customers": db.customers,
        "stocks": db.stocks,
        "stock_history": db.stock_history,
        "transactions": db.transactions,
    }
    await collections["stocks"].create_index([("stock_id", pymongo.ASCENDING)], unique=True)
    await collections["stocks"].create_index([("Company_ticker", pymongo.ASCENDING)], unique=True)
    
    await collections["agents"].create_index([("agent_id", pymongo.ASCENDING)], unique=True)
    return collections

async def get_user():
    db = await get_database()
    User = db.users
    User.create_index([("email", pymongo.ASCENDING)], unique=True)
    return User