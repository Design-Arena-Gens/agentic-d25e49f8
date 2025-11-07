def auth_headers(client):
    client.post("/api/auth/register", json={
        "username": "carol",
        "email": "carol@example.com",
        "password": "supersecret123"
    })
    r = client.post("/api/auth/login", json={
        "email": "carol@example.com",
        "password": "supersecret123"
    })
    tokens = r.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}


def test_experiment_flow(client):
    headers = auth_headers(client)

    # Create agent first
    r = client.post("/api/agents/", json={
        "name": "Bench Agent",
        "framework": "langchain",
        "params": {"temperature": 0.2}
    }, headers=headers)
    assert r.status_code == 200
    agent_id = r.json()["id"]

    # Create experiment
    r = client.post("/api/experiments/", json={
        "agent_id": agent_id,
        "input_data": {"prompt": "Hello"}
    }, headers=headers)
    assert r.status_code == 200, r.text
    exp = r.json()
    assert exp["status"] == "completed"

    # Get experiment
    r = client.get(f"/api/experiments/{exp['id']}", headers=headers)
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "completed"
    assert "result" in body
