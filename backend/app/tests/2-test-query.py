from pymongo import MongoClient

"""
This script connects to a MongoDB database named 'stocksphere' and runs an aggregation pipeline on the 'transactions' collection to identify the top 5 customers based on the total cost of their transactions. The calculation of total cost considers whether transactions are buys or sells, adjusting the cost accordingly.

The aggregation pipeline includes the following steps:
1. Joins 'transactions' with the 'stocks' collection, matching 'ticket' from transactions to 'Company_ticker' in stocks, and storing the result in 'stock_info'.
2. Unwinds the 'stock_info' array to simplify the structure for easier processing in subsequent steps.
3. Joins the modified transactions with the 'customers' collection, matching 'customer_id' to enrich transactions with detailed customer information, stored in 'customer_info'.
4. Unwinds the 'customer_info' to flatten the array for direct access to customer data.
5. Joins the transactions now containing stock and customer details with the 'agents' collection, matching 'agent_id' to add agent details to the transactions, stored in 'agent_info'.
6. Unwinds the 'agent_info' to simplify the document structure, allowing for easier grouping and aggregation.
7. Groups the data by 'customer_id' and calculates the 'total_cost' for each customer. This cost is computed by summing the product of 'volume', 'each_cost', and a conditional factor that is 1 for buys and -1 for sells (based on the 'action' field).
8. Sorts the results by 'total_cost' in descending order to identify customers with the highest transaction costs.
9. Limits the output to the top 5 entries to focus on the highest spenders.
10. Projects the desired fields for the final output, which includes the customer's ID, username, email, total transaction cost, agent's name, and agent's level.

The resulting list displays detailed information about the top 5 customers by transaction cost, providing insights into customer activity, transaction volumes, and the financial impact of their trading actions on the platform.

The output includes:
- Customer ID (derived from MongoDB's grouping `_id`)
- Username
- Email
- Total transaction cost (positive for buys and negative for sells)
- Agent's name
- Agent's level
"""


# Setup MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['stocksphere']  

# Define the MongoDB aggregation pipeline
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
            "total_cost": {
                "$sum": {
                    "$multiply": [
                        "$volume",
                        "$each_cost",
                        {"$cond": [{"$eq": ["$action", "buy"]}, 1, -1]}
                    ]
                }
            },
            "customer_info": {"$first": "$customer_info"},
            "agent_info": {"$first": "$agent_info"}
        }
    },
    {
        "$sort": {"total_cost": -1}
    },
    {"$limit": 5},
    {
        "$project": {
            "customer_id": "$_id",
            "username": "$customer_info.username",
            "email": "$customer_info.email",
            "total_cost": 1,
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