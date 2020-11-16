from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_room():
    response = client.get("/room")
    assert response.status_code == 200

test_room()