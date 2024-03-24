from fastapi.testclient import TestClient
from ..main import app
from ..models import Agent

client = TestClient(app)

def test_create_agent():
    agent_data = {
        "name": "John Doe",
        "contact": "john@example.com",
        "level": "Senior"
    }
    response = client.post("/agents", json=agent_data)
    assert response.status_code == 200
    assert "_id" in response.json()

def test_get_agents():
    response = client.get("/agents")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_agent():
    agent_data = {
        "name": "Jane Smith",
        "contact": "jane@example.com",
        "level": "Junior"
    }
    created_agent = client.post("/agents", json=agent_data).json()
    agent_id = str(created_agent["_id"])

    response = client.get(f"/agents/{agent_id}")
    assert response.status_code == 200
    assert response.json()["_id"] == agent_id

def test_update_agent():
    agent_data = {
        "name": "Mike Johnson",
        "contact": "mike@example.com",
        "level": "Senior"
    }
    created_agent = client.post("/agents", json=agent_data).json()
    agent_id = str(created_agent["_id"])

    updated_agent_data = {
        "name": "Mike Johnson Updated",
        "contact": "mike.updated@example.com"
    }
    response = client.put(f"/agents/{agent_id}", json=updated_agent_data)
    assert response.status_code == 200
    assert response.json()["name"] == updated_agent_data["name"]
    assert response.json()["contact"] == updated_agent_data["contact"]

def test_delete_agent():
    agent_data = {
        "name": "Emily Brown",
        "contact": "emily@example.com",
        "level": "Junior"
    }
    created_agent = client.post("/agents", json=agent_data).json()
    agent_id = str(created_agent["_id"])

    response = client.delete(f"/agents/{agent_id}")
    assert response.status_code == 200
    assert response.json() == True

    response = client.get(f"/agents/{agent_id}")
    assert response.status_code == 404