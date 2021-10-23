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

    response = client.post("/templates", json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_template_by_id(test_db):
    response = client.get("/templates/1")

    assert response.status_code == status.HTTP_200_OK


def test_get_template_not_found(test_db):
    response = client.get("/templates/123")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_templates(test_db):
    response = client.get("/templates")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(data) > 1

    response = client.get("/templates?hospital_id=2")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 1


def test_update_template(test_db):
    payload = {
        "title": "Updated cardiac conditions",
        "headers": "{\"name\":\"string\",\"last_name\":\"string\"}",
    }

    response = client.put("/templates/1", json=payload)
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["title"] == "Updated cardiac conditions"
    assert data["numeric_fields"] == 0
    assert data["alphanumeric_fields"] == 2


def test_delete_template(test_db):
    response = client.delete("/templates/1")

    assert response.status_code == status.HTTP_200_OK

    response = client.get("/templates/1")

    assert response.status_code == status.HTTP_404_NOT_FOUND
