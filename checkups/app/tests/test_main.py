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
    print(data)
    assert response.status_code == 201
    assert data["doctor"]["id"] == 1
    assert data["patient"]["id"] == 1
    assert data["data"] == "{'test':'test'}"
