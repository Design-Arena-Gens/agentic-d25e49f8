def test_register_and_login_flow(client):
    # Register
    r = client.post("/api/auth/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "supersecret123"
    })
    assert r.status_code == 200, r.text
    user = r.json()
    assert user["username"] == "alice"

    # Login
    r = client.post("/api/auth/login", json={
        "email": "alice@example.com",
        "password": "supersecret123"
    })
    assert r.status_code == 200, r.text
    tokens = r.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens

    # Refresh
    r = client.post("/api/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert r.status_code == 200, r.text
    new_tokens = r.json()
    assert new_tokens["access_token"] != tokens["access_token"]

    # Logout
    r = client.post("/api/auth/logout", json={"refresh_token": new_tokens["refresh_token"]})
    assert r.status_code == 200, r.text
