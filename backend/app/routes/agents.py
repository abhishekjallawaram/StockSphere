from fastapi import APIRouter, HTTPException
from app.models import Agent, PyObjectId,Customer
from app.database.mongo import get_collections
from bson import ObjectId
from pymongo.collection import ReturnDocument
from app.utils import authutils
from fastapi import APIRouter, HTTPException, Request,Depends
router = APIRouter()

@router.post("/", response_model=Agent)
async def create_agent(agent: Agent,user: Customer = Depends(authutils.get_current_admin)):
    collections = await get_collections()
    # MongoDB will automatically generate the '_id'
    result = await collections["agents"].insert_one(agent.dict(by_alias=True))
    created_agent = await collections["agents"].find_one({"_id": result.inserted_id})
    return created_agent

@router.get("/", response_model=list[Agent])
async def get_agents(user: Customer = Depends(authutils.get_current_user)):
    collections = await get_collections()
    agents = await collections["agents"].find().to_list(length=100)
    return agents

@router.get("/{agent_id}", response_model=Agent)
async def get_agent(agent_id: int,user: Customer = Depends(authutils.get_current_user)):  # Assuming agent_id is passed as an int in the path
    collections = await get_collections()
    # Adjust query to use 'agent_id' instead of '_id'
    agent = await collections["agents"].find_one({"agent_id": agent_id})
    if agent:
        return agent
    raise HTTPException(status_code=404, detail="Agent not found")

@router.put("/{agent_id}", response_model=Agent)
async def update_agent(agent_id: str, update_data: Agent, user: Customer = Depends(authutils.get_current_admin)):
    collections = await get_collections()
    
    existing_agent = await collections["agents"].find_one({"agent_id": int(agent_id)})
    if not existing_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    update_dict = update_data.dict(exclude_unset=True)
    updated_agent = await collections["agents"].find_one_and_update(
        {"agent_id": int(agent_id)},
        {"$set": update_dict},
        return_document=ReturnDocument.AFTER
    )

    if updated_agent:
        return Agent(**updated_agent)
    else:
        raise HTTPException(status_code=404, detail="Agent update failed")



from typing import List
from pydantic import BaseModel
class agentDeleteRequest(BaseModel):
    agent_ids: List[int]
    
    

@router.delete("/admin", response_model=dict)
async def delete_agent(delete_request: agentDeleteRequest ,user: Customer = Depends(authutils.get_current_admin)):
    agent_ids = delete_request.agent_ids
    collections = await get_collections()
    delete_result = await collections["agents"].delete_many({"agent_id": {"$in": agent_ids}})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="No stocks agents to delete")
    return {"message": f"{delete_result.deleted_count} agents deleted successfully"}

