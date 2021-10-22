from fastapi.testclient import TestClient
from fastapi import status

from main import app
from dependencies import get_db
from tests.test_db import override_get_db, test_db

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_template(test_db):
    payload = {
        "title": "Cardiac conditions",
        "headers": "{\"name\":\"string\",\"last_name\":\"string\",\"condition\":\"string\",\"age\":\"int\"}",
        "specialty_id": 1,
        "hospital_id": 1
    }

    response = client.post("/templates", json=payload)
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED

    assert data["numeric_fields"] == 1
    assert data["alphanumeric_fields"] == 3


def test_get_template_by_id(test_db):
    response = client.get("/templates/1")

    assert response.status_code == status.HTTP_200_OK


def test_get_template_not_found(test_db):
    response = client.get("/templates/123")

    assert response.status_code == status.HTTP_404_NOT_FOUND
