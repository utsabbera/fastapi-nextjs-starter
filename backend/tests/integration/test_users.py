from httpx import AsyncClient


async def test_register_user(client: AsyncClient) -> None:
    response = await client.post(
        "/users",
        json={"email": "test@example.com", "password": "secretpassword"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "hashed_password" not in data


async def test_register_duplicate_email(client: AsyncClient) -> None:
    payload = {"email": "dup@example.com", "password": "password123"}
    await client.post("/users", json=payload)
    response = await client.post("/users", json=payload)
    assert response.status_code == 409


async def test_login(client: AsyncClient) -> None:
    await client.post(
        "/users",
        json={"email": "login@example.com", "password": "mypassword"},
    )
    response = await client.post(
        "/auth/token",
        data={"username": "login@example.com", "password": "mypassword"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
