def auth_headers(client):
    client.post("/api/auth/register", json={
        "username": "bob",
        "email": "bob@example.com",
        "password": "supersecret123"
    })
    r = client.post("/api/auth/login", json={
        "email": "bob@example.com",
        "password": "supersecret123"
    })
    tokens = r.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}


def test_agent_crud(client):
    headers = auth_headers(client)

    # Create
    r = client.post("/api/agents/", json={
        "name": "My Agent",
        "framework": "openai",
        "params": {"model": "gpt-4o-mini"}
    }, headers=headers)
    assert r.status_code == 200, r.text
    agent = r.json()

    # List
    r = client.get("/api/agents/", headers=headers)
    assert r.status_code == 200
    agents = r.json()
    assert len(agents) == 1

    # Get
    r = client.get(f"/api/agents/{agent['id']}", headers=headers)
    assert r.status_code == 200

    # Update
    r = client.put(f"/api/agents/{agent['id']}", json={"name": "Renamed Agent"}, headers=headers)
    assert r.status_code == 200
    assert r.json()["name"] == "Renamed Agent"

    # Delete
    r = client.delete(f"/api/agents/{agent['id']}", headers=headers)
    assert r.status_code == 200

    # Confirm deletion
    r = client.get("/api/agents/", headers=headers)
    assert r.status_code == 200
    assert r.json() == []
