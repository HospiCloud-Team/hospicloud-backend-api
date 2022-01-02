import datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from main import app
from .test_db import test_db

client = TestClient(app)


def test_add_checkup(test_db):
    payload = {
        "data": "{'test':'test'}",
        "doctor_id": 1,
        "patient_id": 1,
        "template_id": 1,
    }
    response = client.post("/checkups/", json=payload)
    data = response.json()
    assert response.status_code == 201
    assert data["doctor"]["id"] == 1
    assert data["patient"]["id"] == 1
    assert data["data"] == "{'test':'test'}"


def test_get_checkups_by_patient(test_db):
    payload = {
        "data": "{'test':'test'}",
        "doctor_id": 1,
        "patient_id": 1,
        "template_id": 1,
    }
    client.post("/checkups/", json=payload)
    response = client.get("/checkups/patient/1")
    data = response.json()
    assert response.status_code == 200
    assert len(data) > 0


def test_get_checkups_by_doctor(test_db):
    payload = {
        "data": "{'test':'test'}",
        "doctor_id": 1,
        "patient_id": 1,
        "template_id": 1,
    }
    client.post("/checkups/", json=payload)
    response = client.get("/checkups/doctor/1")
    data = response.json()
    assert response.status_code == 200
    assert len(data) > 0


def test_create_checkup_with_document_number(test_db):
    payload = {
        "data": "{'test':'test'}",
        "doctor_id": 1,
        "document_number": "12345654321",
        "template_id": 1,
    }

    response = client.post("/checkups/", json=payload)

    data = response.json()

    assert response.status_code == 201
    assert data["doctor"]["id"] == 1
    assert data["patient"]["id"] == 1

def test_create_checkup_with_document_number_missing(test_db):
    payload = {
        "data": "{'test':'test'}",
        "doctor_id": 1,
        "document_number": "14",
        "template_id": 1,
    }

    response = client.post("/checkups/", json=payload)

    assert response.status_code == 404