from motor.motor_asyncio import AsyncIOMotorClient

async def get_mongo_client():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    return client

async def get_database(client):
    return client.stocksphere

async def get_collections():
    client = await get_mongo_client()
    db = client.stocksphere
    collections = {
        "agents": db.agents,
        "customers": db.customers,
        "stocks": db.stocks,
        "stock_history": db.stock_history,
        "transactions": db.transactions,
    }
    return collections