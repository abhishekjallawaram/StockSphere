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
from collections import defaultdict 

router = APIRouter( tags=["Queries"])

    
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

class CustomerTransactionDetail(BaseModel):
    customer_id: int
    username: Optional[str]
    email: Optional[str]
    total_transactions: int
    agent_name: Optional[str]
    agent_level: Optional[str]


@router.get("/customers/most-stock-transactions", response_model=List[CustomerTransactionDetail])
async def get_customers_with_most_stock_transactions(user: Customer = Depends(authutils.get_current_admin)):
    collections = await get_collections()
    transactions = await collections["transactions"].find({"crypto_id": {"$eq": 0}}).to_list(length=None)  # Fetch stock transactions
    customer_ids = {t["customer_id"] for t in transactions if "customer_id" in t}
    agent_ids = {t["agent_id"] for t in transactions if "agent_id" in t}

    # Fetch customer details
    customers = {c["customer_id"]: c for c in await collections["customers"].find({"customer_id": {"$in": list(customer_ids)}}).to_list(length=None)}
    # Fetch agent details
    agents = {a["agent_id"]: a for a in await collections["agents"].find({"agent_id": {"$in": list(agent_ids)}}).to_list(length=None)}

    # Aggregate transactions by customer
    customer_aggregates = {}
    for transaction in transactions:
        customer_id = transaction.get("customer_id")
        if customer_id:
            if customer_id not in customer_aggregates:
                customer_aggregates[customer_id] = {
                    "total_transactions": 0,
                    "customer_info": customers.get(customer_id),
                    "agent_info": agents.get(transaction.get("agent_id"))
                }
            customer_aggregates[customer_id]["total_transactions"] += 1

    # Sort and limit results
    sorted_customers = sorted(customer_aggregates.items(), key=lambda x: x[1]["total_transactions"], reverse=True)[:10]
    
    # Prepare the results
    results = [
        CustomerTransactionDetail(
            customer_id=(key),  # Convert to string here
            username=val["customer_info"]["username"] if val["customer_info"] else None,
            email=val["customer_info"]["email"] if val["customer_info"] else None,
            total_transactions=val["total_transactions"],
            agent_name=val["agent_info"]["name"] if val["agent_info"] else None,
            agent_level=val["agent_info"]["level"] if val["agent_info"] else None
        ) for key, val in sorted_customers
    ]
    return results



class AgentTransactionDetail(BaseModel):
    agent_id: int
    agent_name: Optional[str]
    agent_level: Optional[str]
    total_cost: float

@router.get("/agents/top-stock-transactions", response_model=List[AgentTransactionDetail])
async def get_agents_with_top_stock_transactions(user: Customer = Depends(authutils.get_current_admin)):
    collections = await get_collections()
    transactions = await collections["transactions"].find({"crypto_id": {"$ne": 1}}).to_list(length=None)  # Fetch stock transactions
    agent_ids = {t["agent_id"] for t in transactions if "agent_id" in t}

    # Fetch agent details
    agents = {a["agent_id"]: a for a in await collections["agents"].find({"agent_id": {"$in": list(agent_ids)}}).to_list(length=None)}

    # Aggregate total cost by agent
    agent_totals = {}
    for transaction in transactions:
        agent_id = transaction.get("agent_id")
        if agent_id:
            if agent_id not in agent_totals:
                agent_totals[agent_id] = {
                    "total_cost": 0,
                    "agent_info": agents.get(agent_id)
                }
            volume = transaction.get("volume", 0)
            each_cost = transaction.get("each_cost", 0)
            action = transaction.get("action", "")
            multiplier = 1 if action == "buy" else -1
            total_cost_contribution = volume * each_cost * multiplier

            agent_totals[agent_id]['total_cost'] += total_cost_contribution

    sorted_agents = sorted(agent_totals.items(), key=lambda x: x[1]["total_cost"], reverse=True)[:10]
    

    results = [
        AgentTransactionDetail(
            agent_id=(agent_id),
            agent_name=info["agent_info"]["name"] if info["agent_info"] else None,
            agent_level=info["agent_info"]["level"] if info["agent_info"] else None,
            total_cost=info["total_cost"]
        ) for agent_id, info in sorted_agents
    ]
    
    return results

class CustomerStockTransactionDetail(BaseModel):
    customer_id: int
    username: Optional[str]
    email: Optional[str]
    total_cost: float
    agent_name: Optional[str]
    agent_level: Optional[str]

@router.get("/customers/top-stock-transactions", response_model=List[CustomerStockTransactionDetail])
async def get_customers_with_top_stock_transactions(user: Customer = Depends(authutils.get_current_admin)):
    collections = await get_collections()
    transactions = await collections["transactions"].find({"crypto_id": {"$ne": 0}}).to_list(length=None)  # Fetch stock transactions only
    stocks_dict = {stock['Company_ticker']: stock for stock in await collections["stocks"].find().to_list(length=None)}
    customers_dict = {customer['customer_id']: customer for customer in await collections["customers"].find().to_list(length=None)}
    agents_dict = {agent['agent_id']: agent for agent in await collections["agents"].find().to_list(length=None)}

    customer_aggregates = {}

    # Aggregate total costs by customer
    for transaction in transactions:
        stock_info = stocks_dict.get(transaction.get('ticket'))
        customer_info = customers_dict.get(transaction.get('customer_id'))
        agent_info = agents_dict.get(transaction.get('agent_id'))

        if customer_info and agent_info:
            customer_id = transaction['customer_id']
            if customer_id not in customer_aggregates:
                customer_aggregates[customer_id] = {
                    'total_cost': 0,
                    'customer_info': customer_info,
                    'agent_info': agent_info
                }
            
            volume = transaction.get('volume', 0)
            each_cost = transaction.get('each_cost', 0)
            action_multiplier = 1 if transaction.get('action') == 'buy' else -1
            total_cost = volume * each_cost * action_multiplier

            customer_aggregates[customer_id]['total_cost'] += total_cost

    # Sort and limit results
    limit = 10
    sorted_customers = sorted(customer_aggregates.items(), key=lambda x: x[1]['total_cost'], reverse=True)[:limit]
    
    # Prepare the results
    results = [
        CustomerStockTransactionDetail(
            customer_id=(cust_id),
            username=cust['customer_info']['username'],
            email=cust['customer_info']['email'],
            total_cost=cust['total_cost'],
            agent_name=cust['agent_info']['name'] if cust['agent_info'] else None,
            agent_level=cust['agent_info']['level'] if cust['agent_info'] else None
        ) for cust_id, cust in sorted_customers
    ]
    
    return results


class CustomerCryptoTransactionDetail(BaseModel):
    customer_id: int
    username: Optional[str]
    email: Optional[str]
    total_cost: float
    agent_name: Optional[str]
    agent_level: Optional[str]

@router.get("/customers/top-crypto-transactions", response_model=List[CustomerCryptoTransactionDetail])
async def get_customers_with_top_crypto_transactions(user: Customer = Depends(authutils.get_current_admin)):
    collections = await get_collections()
    transactions = await collections["transactions"].find({"stock_id": {"$ne": 1}}).to_list(length=None)  # Fetch crypto transactions only

    # Load necessary data from related collections
    crypto_dict = {crypto['Symbol']: crypto for crypto in await collections["cryptocurrencies"].find().to_list(length=None)}
    customers_dict = {customer['customer_id']: customer for customer in await collections["customers"].find().to_list(length=None)}
    agents_dict = {agent['agent_id']: agent for agent in await collections["agents"].find().to_list(length=None)}

    customer_aggregates = {}

    # Aggregate total costs by customer
    for transaction in transactions:
        crypto_info = crypto_dict.get(transaction.get('ticket'))
        customer_info = customers_dict.get(transaction.get('customer_id'))
        agent_info = agents_dict.get(transaction.get('agent_id'))

        if customer_info and agent_info:
            customer_id = transaction['customer_id']
            if customer_id not in customer_aggregates:
                customer_aggregates[customer_id] = {
                    'total_cost': 0,
                    'customer_info': customer_info,
                    'agent_info': agent_info
                }
            
            volume = transaction.get('volume', 0)
            each_cost = transaction.get('each_cost', 0)
            action_multiplier = 1 if transaction.get('action') == 'buy' else -1
            total_cost = volume * each_cost * action_multiplier

            customer_aggregates[customer_id]['total_cost'] += total_cost

    # Sort and limit the results
    limit = 10
    sorted_customers = sorted(customer_aggregates.items(), key=lambda x: x[1]['total_cost'], reverse=True)[:limit]
    
    # Prepare the results
    results = [
        CustomerCryptoTransactionDetail(
            customer_id=(cust_id),
            username=cust['customer_info']['username'],
            email=cust['customer_info']['email'],
            total_cost=cust['total_cost'],
            agent_name=cust['agent_info']['name'] if cust['agent_info'] else None,
            agent_level=cust['agent_info']['level'] if cust['agent_info'] else None
        ) for cust_id, cust in sorted_customers
    ]
    
    return results



class AgentCryptoTransactionDetail(BaseModel):
    agent_id: int
    agent_name: Optional[str]
    agent_level: Optional[str]
    total_cost: float

@router.get("/agents/top-crypto-transactions", response_model=List[AgentCryptoTransactionDetail])
async def get_agents_with_top_crypto_transactions(user: Customer = Depends(authutils.get_current_admin)):
    collections = await get_collections()
    transactions = await collections["transactions"].find({"stock_id": {"$ne": 1}}).to_list(length=None)  # Fetch crypto transactions only
    agent_ids = {t["agent_id"] for t in transactions if "agent_id" in t}

    # Fetch agent details
    agents = {a["agent_id"]: a for a in await collections["agents"].find({"agent_id": {"$in": list(agent_ids)}}).to_list(length=None)}

    # Aggregate total cost by agent
    agent_totals = {}
    for transaction in transactions:
        agent_id = transaction.get("agent_id")
        if agent_id:
            if agent_id not in agent_totals:
                agent_totals[agent_id] = {
                    "total_cost": 0,
                    "agent_info": agents.get(agent_id)
                }
            volume = transaction.get("volume", 0)
            each_cost = transaction.get("each_cost", 0)
            action = transaction.get("action", "")
            multiplier = 1 if action == "buy" else -1
            total_cost_contribution = volume * each_cost * multiplier

            agent_totals[agent_id]['total_cost'] += total_cost_contribution

    # Sort and limit results
    limit = 10
    sorted_agents = sorted(agent_totals.items(), key=lambda x: x[1]["total_cost"], reverse=True)[:limit]
    
    # Prepare the results
    results = [
        AgentCryptoTransactionDetail(
            agent_id=(agent_id),
            agent_name=info["agent_info"]["name"] if info["agent_info"] else None,
            agent_level=info["agent_info"]["level"] if info["agent_info"] else None,
            total_cost=info["total_cost"]
        ) for agent_id, info in sorted_agents
    ]
    
    return results


class CustomerCryptoTransactionCount(BaseModel):
    customer_id: int
    username: Optional[str]
    email: Optional[str]
    total_transactions: int
    agent_name: Optional[str]
    agent_level: Optional[str]

@router.get("/customers/most-crypto-transactions", response_model=List[CustomerCryptoTransactionCount])
async def get_customers_with_most_crypto_transactions(user: Customer = Depends(authutils.get_current_admin)):
    collections = await get_collections()
    transactions = await collections["transactions"].find({"stock_id": {"$ne": 1}}).to_list(length=None)  # Fetch crypto transactions only
    customer_ids = {t["customer_id"] for t in transactions if "customer_id" in t}
    agent_ids = {t["agent_id"] for t in transactions if "agent_id" in t}

    # Fetch customer and agent details
    customers = {c["customer_id"]: c for c in await collections["customers"].find({"customer_id": {"$in": list(customer_ids)}}).to_list(length=None)}
    agents = {a["agent_id"]: a for a in await collections["agents"].find({"agent_id": {"$in": list(agent_ids)}}).to_list(length=None)}

    # Aggregate transactions by customer
    grouped_data = defaultdict(lambda: {'total_transactions': 0, 'customer_info': None, 'agent_info': None})
    for transaction in transactions:
        customer_id = transaction.get("customer_id")
        if customer_id:
            grouped_data[customer_id]['total_transactions'] += 1
            grouped_data[customer_id]['customer_info'] = customers.get(customer_id)
            grouped_data[customer_id]['agent_info'] = agents.get(transaction.get("agent_id"))

    # Sort and limit results
    limit = 10
    sorted_customers = sorted(grouped_data.items(), key=lambda x: x[1]['total_transactions'], reverse=True)[:limit]
    
    # Prepare the results
    results = [
        CustomerCryptoTransactionCount(
            customer_id=(key),
            username=val['customer_info']['username'] if val['customer_info'] else None,
            email=val['customer_info']['email'] if val['customer_info'] else None,
            total_transactions=val['total_transactions'],
            agent_name=val['agent_info']['name'] if val['agent_info'] else None,
            agent_level=val['agent_info']['level'] if val['agent_info'] else None
        ) for key, val in sorted_customers
    ]
    
    return results