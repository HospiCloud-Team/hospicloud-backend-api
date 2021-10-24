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


def test_get_specialty_by_id(test_db):
    response = client.get("/specialties/1")

    assert response.status_code == status.HTTP_200_OK


def test_get_specialty_not_found(test_db):
    response = client.get("/specialties/123")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_specialty(test_db):
    response = client.delete("/specialties/1")

    assert response.status_code == status.HTTP_200_OK


def test_update_specialty(test_db):
    payload = {
        "name": "updated specialty"
    }

    response = client.put("/specialties/2", json=payload)
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["name"] == "updated specialty"
