import enum
import datetime
from .database import start_engine
from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.sql.sqltypes import Boolean, Time
from sqlalchemy.types import JSON, DateTime, Date, CHAR, Enum, Integer, String
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

doctor_to_specialty_association = Table(
    "doctor_specialty",
    Base.metadata,
    Column("doctor_id", ForeignKey("doctor.id")),
    Column("specialty_id", ForeignKey("specialty.id")),
)

hospital_to_specialty_association = Table(
    "hospital_specialty",
    Base.metadata,
    Column("hospital_id", ForeignKey("hospital.id")),
    Column("specialty_id", ForeignKey("specialty.id")),
)


class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", uselist=False)
    hospital_id = Column(Integer, ForeignKey("hospital.id"))


class Checkup(Base):
    __tablename__ = "checkup"
    id = Column(Integer, primary_key=True)
    template_id = Column(Integer, ForeignKey("template.id"))
    doctor_id = Column(Integer, ForeignKey("doctor.id"))
    patient_id = Column(Integer, ForeignKey("patient.id"))
    data = Column(JSON)
    date = Column(DateTime, default=datetime.datetime.now())
    patient = relationship("Patient", back_populates="checkups")
    doctor = relationship("Doctor", back_populates="checkups")


class Province(enum.Enum):
    azua = 1
    bahoruco = 2
    barahona = 3
    dajabon = 4
    distrito_nacional = 5
    duarte = 6
    elias_pina = 7
    el_seibo = 8
    espaillat = 9
    hato_mayor = 10
    hermanas_mirabal = 11
    independencia = 12
    la_altagracia = 13
    la_romana = 14
    la_vega = 15
    maria_trinidad_sanchez = 16
    monsenor_nouel = 17
    monte_cristi = 18
    monte_plata = 19
    pedernales = 20
    peravia = 21
    puerto_plata = 22
    samana = 23
    sanchez_ramirez = 24
    san_cristobal = 25
    san_jose_de_ocoa = 26
    san_juan = 27
    san_pedro_de_macoris = 28
    santiago = 29
    santiago_rodriguez = 30
    santo_domingo = 31
    valverde = 32


class City(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True)
    province_id = Column(Enum(Province))
    address = Column(String)


class Doctor(Base):
    __tablename__ = "doctor"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", uselist=False)
    hospital_id = Column(Integer, ForeignKey("hospital.id"))
    schedule_id = Column(Integer, ForeignKey("schedule.id"))
    specialties = relationship(
        "Specialty", secondary=doctor_to_specialty_association, back_populates="doctors"
    )
    checkups = relationship("Checkup")


class Hospital(Base):
    __tablename__ = "hospital"
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey("location.id"))
    schedule_id = Column(Integer, ForeignKey("schedule.id"))
    name = Column(String)
    specialties = relationship(
        "Specialty",
        secondary=hospital_to_specialty_association,
        back_populates="hospitals",
    )
    created_at = Column(DateTime, default=datetime.datetime.now())
    created_by = Column(Integer, ForeignKey("user.id"))
    updated_at = Column(DateTime)
    updated_by = Column(Integer, ForeignKey("user.id"))


class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    address = Column(String)


class BloodType(str, enum.Enum):
    a_plus = "a_plus"
    a_minus = "a_minus"
    b_plus = "b_plus"
    b_minus = "b_minus"
    o_plus = "o_plus"
    o_minus = "o_minus"
    ab_plus = "ab_plus"
    ab_minus = "ab_minus"


class Patient(Base):
    __tablename__ = "patient"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", uselist=False)
    id_blood_type = Column(Enum(BloodType))
    medical_background = Column(String)
    checkups = relationship("Checkup")


class Specialty(Base):
    __tablename__ = "specialty"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    doctors = relationship("Doctor", secondary=doctor_to_specialty_association, back_populates="specialties")
    hospitals = relationship("Hospital", secondary=hospital_to_specialty_association, back_populates="specialties")


class Template(Base):
    __tablename__ = "template"
    id = Column(Integer, primary_key=True)
    specialty_id = Column(Integer, ForeignKey("specialty.id"))
    hospital_id = Column(Integer, ForeignKey("hospital.id"))
    numeric_fields = Column(Integer)
    alphanumeric_fields = Column(Integer)
    file_upload_fields = Column(Integer)
    headers = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.now())
    created_by = Column(Integer, ForeignKey("user.id"))
    updated_at = Column(DateTime)
    updated_by = Column(Integer, ForeignKey("user.id"))


class Schedule(Base):
    __tablename__ = "schedule"
    id = Column(Integer, primary_key=True)
    start_day = Column(String)
    end_day = Column(String)
    start_time = Column(Time)
    end_time = Column(Time)
    all_day = Column(Boolean, default=False)


class UserRole(str, enum.Enum):
    admin = "admin"
    doctor = "doctor"
    patient = "patient"


class DocumentType(str, enum.Enum):
    national_id = "national_id"
    passport = "passport"


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    user_role = Column(Enum(UserRole))
    document_type = Column(Enum(DocumentType))
    name = Column(String(length=50))
    last_name = Column(String(length=50))
    password = Column(String)
    email = Column(String, unique=True)
    document_number = Column(String(11))
    date_of_birth = Column(Date)
    created_at = Column(DateTime, default=datetime.datetime.now())
    created_by = Column(Integer, ForeignKey("user.id"))
    updated_at = Column(DateTime)
    updated_by = Column(Integer, ForeignKey("user.id"))

engine = start_engine()

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"


def create_tables():
    #Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
