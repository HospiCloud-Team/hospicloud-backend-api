from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from common.database import start_engine
from common.models import Base, Template, Specialty, Hospital

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    templates = [
        Template(
            title="Mock template",
            headers="{\"name\":\"string\",\"last_name\":\"string\",\"condition\":\"string\",\"age\":\"int\"}",
            specialty_id=2,
            hospital_id=1,
            numeric_fields=1,
            alphanumeric_fields=3
        ),
        Template(
            title="Mock template",
            headers="{\"name\":\"string\",\"last_name\":\"string\",\"condition\":\"string\",\"age\":\"int\"}",
            specialty_id=2,
            hospital_id=2,
            numeric_fields=1,
            alphanumeric_fields=3
        )
    ]

    hospitals = [
        Hospital(name="Mock hospital"),
        Hospital(name="Private hospital")
    ]
    specialties = [
        Specialty(name="pediatrician", hospital_id=1),
        Specialty(name="general", hospital_id=2),
        Specialty(name="mortician", hospital_id=2)
    ]

    db.bulk_save_objects(hospitals)
    db.bulk_save_objects(specialties)
    db.bulk_save_objects(templates)
    db.commit()

    yield
    Base.metadata.drop_all(bind=engine)
