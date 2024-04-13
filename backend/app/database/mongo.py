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
        "cryptocurrencies" : db.cryptocurrencies,
        "crypto_history" : db.crypto_history
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




from fastapi import FastAPI, WebSocket
from pymongo import MongoClient
from starlette.websockets import WebSocketDisconnect

app = FastAPI()

# # Initialize MongoDB client and specify your database and collection
client = MongoClient("mongodb://localhost:27017")
db = client["stocksphere"]

connected_clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        # MongoDB Change Stream
        with db.watch() as stream:
            for change in stream:
                # Broadcast the change to all connected WebSocket clients
                for client in connected_clients:
                    await client.send_json(change)
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        print("Client disconnected")
