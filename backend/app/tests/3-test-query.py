from pymongo import MongoClient

# Connect to MongoDB - Replace 'localhost' and '27017' with your MongoDB host and port if different
client = MongoClient('mongodb://localhost:27017/')

# Assuming your database name is 'mydatabase'
db = client['stocksphere']  

# Define the MongoDB aggregation pipeline for top agents
pipeline = [
    {
        "$lookup": {
            "from": "stocks",  # Assuming this is the name of your stocks collection
            "localField": "ticket",
            "foreignField": "Company_ticker",  # Matching ticket to Company_ticker
            "as": "stock_info"
        }
    },
    {"$unwind": "$stock_info"},  # Unwind the resulting array to simplify processing
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
            "_id": "$agent_id",
            "total_cost": {
                "$sum": {
                    "$multiply": [
                        "$volume",
                        "$each_cost",
                        {"$cond": [{"$eq": ["$action", "buy"]}, 1, -1]}
                    ]
                }
            },
            "agent_info": {"$first": "$agent_info"}
        }
    },
    {
        "$sort": {"total_cost": -1}
    },
    {"$limit": 5},
    {
        "$project": {
            "agent_id": "$_id",
            "agent_name": "$agent_info.name",
            "agent_level": "$agent_info.level",
            "total_cost": 1
        }
    }
]

# Execute the query
top_agents = list(db.transactions.aggregate(pipeline))

# Printing the results
for agent in top_agents:
    print(agent)
