from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_index():
    response = client.get("/")
    assert response.status_code == 200


# def test_auth():
#     test_data = {
#         "valid": {"username": "testuser123", "password": "Testuser123"},
#         "invalid": {"username": "nonexistuser", "password": "meaninglesspass"},
#     }
#
#     # Send the POST request
#     response = client.post("api/v01/login/auth/", data=test_data["valid"])
#
#     assert response.status_code == status.HTTP_200_OK
#     assert isinstance(response.content, bytes)
#
#     # Send the POST request
#     response = client.post("api/v01/login/auth/", data=test_data["invalid"])
#
#     assert response.status_code == status.HTTP_404_NOT_FOUND
