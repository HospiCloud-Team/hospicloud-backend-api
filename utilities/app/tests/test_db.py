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

    template = Template(
        title="Cardiac conditions",
        headers="{\"name\":\"string\",\"last_name\":\"string\",\"condition\":\"string\",\"age\":\"int\"}",
        specialty_id=1,
        hospital_id=1,
        numeric_fields=1,
        alphanumeric_fields=3
    )

    hospital = Hospital(name="Mock hospital")
    specialty = Specialty(name="pediatrician")

    db.add(hospital)
    db.add(specialty)
    db.add(template)
    db.commit()

    yield
    Base.metadata.drop_all(bind=engine)
