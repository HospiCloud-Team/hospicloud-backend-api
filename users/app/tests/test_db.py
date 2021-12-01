import datetime
from typing import List
from pydantic.main import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from common.database import start_engine
from common.models import Base, Hospital, User, Patient, Specialty, Doctor, Admin
from common.schemas.auth import FirebaseUser
from common.schemas.user import UserRole

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class CurrentUser(BaseModel):
    email: str
    uid: str


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def override_get_current_user():
    return FirebaseUser(
        email="test.admin@gmail.com",
        uid="1",
        user_role=UserRole.admin,
        hospital_id=1,
    )


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    admin_user = User(
        user_role="admin",
        document_type="national_id",
        name="test",
        last_name="test",
        email="test.admin@gmail.com",
        document_number="13345678931",
        date_of_birth=datetime.datetime.strptime("01-20-2000", "%m-%d-%Y"),
        created_at=datetime.datetime.now(datetime.timezone.utc),
    )

    admin = Admin(hospital_id=1)

    patient_user = User(
        user_role="patient",
        document_type="national_id",
        name="test",
        last_name="test",
        email="test@gmail.com",
        document_number="12345654321",
        date_of_birth=datetime.datetime.strptime("01-20-2000", "%m-%d-%Y"),
        created_at=datetime.datetime.now(datetime.timezone.utc),
    )

    patient = Patient(user=patient_user, blood_type="a_plus")

    doctor_users: List[User] = [
        User(
            user_role="doctor",
            document_type="national_id",
            name="Alejandro",
            last_name="Smith",
            email="test.doctor@gmail.com",
            document_number="12345654321",
            date_of_birth=datetime.datetime.strptime("01-20-2000", "%m-%d-%Y"),
        ),
        User(
            user_role="doctor",
            document_type="national_id",
            name="Alejandro",
            last_name="Smith",
            email="test.doctor2@gmail.com",
            document_number="12345654321",
            date_of_birth=datetime.datetime.strptime("01-20-2000", "%m-%d-%Y"),
        ),
    ]

    doctors = [
        Doctor(user_id=2, hospital_id=1, schedule="L, X, V 8:00 - 12:00, 4:00 - 6:00"),
        Doctor(user_id=3, hospital_id=1, schedule="L, X, V 8:00 - 12:00, 4:00 - 6:00"),
    ]

    hospital = Hospital(
        name="Mock hospital",
        description="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    )

    specialties = [
        Specialty(name="pediatrician", hospital_id=1),
        Specialty(name="general", hospital_id=1),
    ]

    db.add(admin_user)
    db.add(admin)
    db.add(patient_user)
    db.add(patient)
    db.add(hospital)
    db.bulk_save_objects(specialties)
    db.add_all(doctor_users)
    db.add_all(doctors)
    db.commit()

    yield
    Base.metadata.drop_all(bind=engine)
