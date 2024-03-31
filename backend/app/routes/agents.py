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
async def update_agent(agent_id: int, update_data: Agent,user: Customer = Depends(authutils.get_current_admin)):  # Assuming agent_id is passed as an int in the path
    collections = await get_collections()
    update_data_dict = {
        k: v for k, v in update_data.model_dump(by_alias=True).items() if v is not None
    }

    if len(update_data_dict) >= 1:
        update_result = await collections["agents"].find_one_and_update(
            {"_id": ObjectId(agent_id)},  
            return_document=ReturnDocument.AFTER,
        )
        if update_result:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")

    # The update is empty, but we should still return the matching document if it exists.
    if (existing_agent := await collections["agents"].find_one({"_id": ObjectId(agent_id)})) is not None:
        return existing_agent

    raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")

@router.delete("/{agent_id}", response_model=bool)
async def delete_agent(agent_id: int,user: Customer = Depends(authutils.get_current_admin)): 
    collections = await get_collections()
    result = await collections["agents"].delete_one({"agent_id": agent_id})
    if result.deleted_count:
        return True
    raise HTTPException(status_code=404, detail="Agent not found")
