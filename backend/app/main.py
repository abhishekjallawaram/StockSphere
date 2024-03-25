from fastapi import FastAPI
from app.routes import agents, customers, stocks, stock_history, transactions
from app.database.mongo import MongoDB
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth


app = FastAPI()

app.include_router(agents.router, prefix="/agents", tags=["agents"])
# app.include_router(customers.router, prefix="/customers", tags=["customers"])
# app.include_router(stocks.router, prefix="/stocks", tags=["stocks"])
# app.include_router(stock_history.router, prefix="/stock-history", tags=["stock-history"])
# app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to 2FA Authentication with FastAPI"}

# @app.on_event("startup")
# async def startup_event():
#     app.state.mongo_client = MongoDB.get_client()
#     app.state.mongo_db = app.state.mongo_client.stocksphere
#     app.state.mongo_collections = {
#         "agents": app.state.mongo_db.agents,
#         "customers": app.state.mongo_db.customers,
#         "stocks": app.state.mongo_db.stocks,
#         "stock_history": app.state.mongo_db.stock_history,
#         "transactions": app.state.mongo_db.transactions,
#     }

# @app.on_event("shutdown")
# async def shutdown_event():
#     app.state.mongo_client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)