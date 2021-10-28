from fastapi.testclient import TestClient
from fastapi import status

from main import app
from dependencies import get_db
from tests.test_db import override_get_db, test_db

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_hospital(test_db):
    payload = {
        "name": "Public hospital",
        "schedule": "L, X, V 8:00 - 12:00, 4:00 - 6:00",
        "location": {
            "address": "Av. Abraham Lincoln 2, Santo Domingo 10101",
            "province": "santo_domingo"
        }
    }

    response = client.post("/hospitals", json=payload)
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED


def test_get_hospital_by_id(test_db):
    response = client.get("/hospitals/1")

    assert response.status_code == status.HTTP_200_OK


def test_get_hospital_by_id_not_found(test_db):
    response = client.get("/hospitals/123")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_hospitals(test_db):
    response = client.get("/hospitals")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(data) > 1
