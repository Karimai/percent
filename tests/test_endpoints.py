from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_index():
    response = client.get("/")
    assert response.status_code == 200


# def test_auth_endpoint():
#     # Test user data
#     test_user = {"username": "testuser123", "password": "Testuser123"}
#
#     # Send a POST request to the /auth/ endpoint
#     response = client.post("/login/auth/", data=test_user)
#
#     # Check if the response status code is 200 OK
#     assert response.status_code == 200
#
#     # Check if the response contains the expected keys
#     assert "access_token" in response.json()
#     response_data = response.json()
#     assert response_data["token_type"] == "bearer"
