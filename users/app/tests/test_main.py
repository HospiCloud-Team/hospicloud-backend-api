from fastapi.testclient import TestClient
from fastapi import responses, status
from main import app
from dependencies import get_db, get_current_user
from tests.test_db import test_db, override_get_db, override_get_current_user

app.dependency_overrides[get_db] = override_get_db

app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


def test_register(test_db):
    payload = {
        "user_role": "patient",
        "document_type": "national_id",
        "name": "Frank",
        "last_name": "Chavez",
        "email": "frankroberto@gmail.com",
        "document_number": "22222222222",
        "date_of_birth": "2000-01-20",
        "patient": {"medical_background": "Test description", "blood_type": "a_plus"},
    }

    response = client.post("/register?test=True", json=payload)
    print(response.json())
    assert response.status_code == status.HTTP_201_CREATED


def test_create_doctor(test_db):
    payload = {
        "user_role": "doctor",
        "document_type": "national_id",
        "name": "Alejandro",
        "last_name": "del Toro",
        "email": "alejandro79@gmail.com",
        "document_number": "11111111111",
        "date_of_birth": "2000-06-27",
        "doctor": {
            "schedule": "L, X, V 8:00 - 12:00, 4:00 - 6:00",
            "hospital_id": 1,
            "specialty_ids": [1, 2],
        },
    }

    response = client.post(
        "/users?test=True",
        json=payload,
        headers={"Authorization": "Bearer test-token"},
    )
    data: dict = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data["doctor"] is not None
    assert data["doctor"]["specialties"] is not None
    assert len(data["doctor"]["specialties"]) == 2


def test_create_admin(test_db):
    payload = {
        "user_role": "admin",
        "document_type": "national_id",
        "name": "Alejandro",
        "last_name": "del Toro",
        "email": "alejandro79@gmail.com",
        "document_number": "11111111111",
        "date_of_birth": "2000-06-27",
        "admin": {"hospital_id": 1},
    }

    response = client.post(
        "/users?test=True",
        json=payload,
        headers={"Authorization": "Bearer test-token"},
    )

    assert response.status_code == status.HTTP_201_CREATED


def test_create_user_email_already_exists(test_db):
    payload = {
        "user_role": "admin",
        "document_type": "national_id",
        "name": "Alejandro",
        "last_name": "del Toro",
        "email": "alejandro79@gmail.com",
        "document_number": "11111111111",
        "date_of_birth": "2000-06-27",
        "admin": {"hospital_id": 1},
    }

    _ = client.post("/users?test=True", json=payload)
    response = client.post(
        "/users?test=True",
        json=payload,
        headers={"Authorization": "Bearer test-token"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_user_by_id(test_db):
    response = client.get(
        "/users/1",
        headers={"Authorization": "Bearer test-token"},
    )

    assert response.status_code == status.HTTP_200_OK


def test_get_user_not_found(test_db):
    response = client.get(
        "/users/123",
        headers={"Authorization": "Bearer test-token"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_users_list(test_db):
    response = client.get(
        "/users",
        headers={"Authorization": "Bearer test-token"},
    )
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(data) > 0


def test_delete_user(test_db):
    response = client.delete(
        "/users/1?test=True",
        headers={"Authorization": "Bearer test-token"},
    )

    assert response.status_code == status.HTTP_200_OK

    response = client.get(
        "/users/1",
        headers={"Authorization": "Bearer test-token"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_user(test_db):
    payload = {
        "name": "new name",
        "last_name": "new last name",
        "document_number": "12345654399",
    }

    response = client.put(
        "/users/1",
        json=payload,
        headers={"Authorization": "Bearer test-token"},
    )
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["name"] == "new name"
    assert data["last_name"] == "new last name"
    assert data["document_number"] == "12345654399"
    assert data["updated_at"] is not None


def test_get_doctors_by_hospital_id(test_db):
    response = client.get(
        "/users/doctors?hospital_id=1",
        headers={"Authorization": "Bearer test-token"},
    )
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 2
