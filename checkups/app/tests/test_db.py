import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from main import app
from common.database import start_engine
from common.models import Base, User, Patient, Doctor, Template
from dependencies import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    doctor_user = User(
        user_role="doctor",
        document_type="national_id",
        name="test",
        last_name="test",
        email="test@doctor",
        document_number="12345654321",
        date_of_birth=datetime.datetime.strptime("01-20-2000", "%m-%d-%Y"),
    )
    patient_user = User(
        document_type="national_id",
        name="test",
        last_name="test",
        email="test@patient",
        document_number="12345654321",
        date_of_birth=datetime.datetime.strptime("01-20-2000", "%m-%d-%Y"),
    )
    doctor = Doctor(user=doctor_user)
    patient = Patient(user=patient_user, id_blood_type="a_plus")
    template = Template(
        numeric_fields=0,
        alphanumeric_fields=1,
        file_upload_fields=0,
        headers="{'test':'str'}",
    )
    db.add(doctor_user)
    db.add(patient_user)
    db.add(doctor)
    db.add(patient)
    db.add(template)
    db.commit()
    db.refresh(doctor)
    db.refresh(patient)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
