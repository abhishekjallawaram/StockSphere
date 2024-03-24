from fastapi import APIRouter, HTTPException
from ..models import Agent
from ..database.mongo import get_collections

router = APIRouter()

@router.post("/", response_model=Agent)
async def create_agent(agent: Agent):
    collections = await get_collections()
    result = await collections["agents"].insert_one(agent.dict())
    created_agent = await collections["agents"].find_one({"_id": result.inserted_id})
    return created_agent

@router.get("/", response_model=list[Agent])
async def get_agents():
    collections = await get_collections()
    agents = await collections["agents"].find().to_list(length=100)
    return agents

@router.get("/{agent_id}", response_model=Agent)
async def get_agent(agent_id: str):
    collections = await get_collections()
    agent = await collections["agents"].find_one({"_id": PyObjectId(agent_id)})
    if agent:
        return agent
    raise HTTPException(status_code=404, detail="Agent not found")

@router.put("/{agent_id}", response_model=Agent)
async def update_agent(agent_id: str, agent: Agent):
    collections = await get_collections()
    result = await collections["agents"].update_one(
        {"_id": PyObjectId(agent_id)},
        {"$set": agent.dict(exclude_unset=True)}
    )
    if result.modified_count:
        updated_agent = await collections["agents"].find_one({"_id": PyObjectId(agent_id)})
        return updated_agent
    raise HTTPException(status_code=404, detail="Agent not found")

@router.delete("/{agent_id}", response_model=bool)
async def delete_agent(agent_id: str):
    collections = await get_collections()
    result = await collections["agents"].delete_one({"_id": PyObjectId(agent_id)})
    if result.deleted_count:
        return True
    raise HTTPException(status_code=404, detail="Agent not found")