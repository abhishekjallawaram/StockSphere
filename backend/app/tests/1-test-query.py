from pymongo import MongoClient


# Setup MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['stocksphere']  # Replace with your actual database name

# Define the MongoDB aggregation pipeline
pipeline = [
    {
        "$lookup": {
            "from": "stocks",  # This must be the actual name of your stocks collection
            "localField": "ticket",
            "foreignField": "Company_ticker",  # Matching ticket to Company_ticker
            "as": "stock_info"
        }
    },
    {"$unwind": "$stock_info"},  # Unwind the resulting array to simplify processing
    {
        "$lookup": {
            "from": "customers",  # The actual name of your customers collection
            "localField": "customer_id",
            "foreignField": "customer_id",  # Match customer_id from Transaction to Customer
            "as": "customer_info"
        }
    },
    {"$unwind": "$customer_info"},
    {
        "$lookup": {
            "from": "agents",  # The actual name of your agents collection
            "localField": "agent_id",
            "foreignField": "agent_id",  # Match agent_id from Transaction to Agent
            "as": "agent_info"
        }
    },
    {"$unwind": "$agent_info"},
    {
        "$group": {
            "_id": "$customer_id",
            "total_transactions": {"$sum": 1},
            "customer_info": {"$first": "$customer_info"},
            "agent_info": {"$first": "$agent_info"}
        }
    },
    {
        "$sort": {"total_transactions": -1}
    },
    {"$limit": 5},
    {
        "$project": {
            "customer_id": "$_id",
            "username": "$customer_info.username",
            "email": "$customer_info.email",
            "total_transactions": 1,
            "agent_name": "$agent_info.name",
            "agent_level": "$agent_info.level"
        }
    }
]

# Execute the query
top_customers = list(db.transactions.aggregate(pipeline))

# Printing the results
for customer in top_customers:
    print(customer)