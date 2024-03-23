from motor.motor_asyncio import AsyncIOMotorClient

async def get_mongo_client():
    mongo_uri = "mongodb://stocksphere-mongodb:27017"
    client = AsyncIOMotorClient(mongo_uri)
    return client

async def get_database(client):
    return client.stocksphere

async def get_collections(db):
    collections = {
        "stocks": db.stocks,
        "stock_history": db.stock_history,
        "transactions": db.transactions,
        "agents": db.agents,
        "customers": db.customers,
    }
    return collections