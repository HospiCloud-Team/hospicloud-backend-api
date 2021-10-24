from fastapi.testclient import TestClient
from fastapi import status

from main import app
from dependencies import get_db
from tests.test_db import override_get_db, test_db

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_specialty(test_db):
    payload = {
        "name": "oftalmologist",
        "hospital_id": 1
    }

    response = client.post("/specialties", json=payload)

    assert response.status_code == status.HTTP_201_CREATED

