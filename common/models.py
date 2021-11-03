import enum
import datetime
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.sql import func
from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import JSON, DateTime, Date, Enum, Integer, String, Boolean, Time
from sqlalchemy.orm import backref, declarative_base, relationship, sessionmaker, Session

from common.database import start_engine

Base = declarative_base()

doctor_to_specialty_association = Table(
    "doctor_specialty",
    Base.metadata,
    Column("doctor_id", ForeignKey("doctor.id")),
    Column("specialty_id", ForeignKey("specialty.id")),
)


class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    hospital_id = Column(Integer, ForeignKey("hospital.id"))

    user = relationship(
        "User",
        uselist=False
    )


class Checkup(Base):
    __tablename__ = "checkup"
    id = Column(Integer, primary_key=True)
    template_id = Column(Integer, ForeignKey("template.id"))
    doctor_id = Column(Integer, ForeignKey("doctor.id"))
    patient_id = Column(Integer, ForeignKey("patient.id"))
    data = Column(JSON)
    date = Column(DateTime, default=datetime.datetime.now())
    patient = relationship(
        "Patient", back_populates="checkups", lazy="joined", join_depth=2)
    doctor = relationship(
        "Doctor", back_populates="checkups", lazy="joined", join_depth=2)


class Province(str, enum.Enum):
    azua = "azua"
    bahoruco = "bahoruco"
    barahona = "barahona"
    dajabon = "dajabon"
    distrito_nacional = "distrito_nacional"
    duarte = "duarte"
    elias_pina = "elias_pina"
    el_seibo = "el_seibo"
    espaillat = "espaillat"
    hato_mayor = "hato_mayor"
    hermanas_mirabal = "hermanas_mirabal"
    independencia = "independencia"
    la_altagracia = "la_altagracia"
    la_romana = "la_romana"
    la_vega = "la_vega"
    maria_trinidad_sanchez = "maria_trinidad_sanchez"
    monsenor_nouel = "monsenor_nouel"
    monte_cristi = "monte_cristi"
    monte_plata = "monte_plata"
    pedernales = "pedernales"
    peravia = "peravia"
    puerto_plata = "puerto_plata"
    samana = "samana"
    sanchez_ramirez = "sanchez_ramirez"
    san_cristobal = "san_cristobal"
    san_jose_de_ocoa = "san_jose_de_ocoa"
    san_juan = "san_juan"
    san_pedro_de_macoris = "san_pedro_de_macoris"
    santiago = "santiago"
    santiago_rodriguez = "santiago_rodriguez"
    santo_domingo = "santo_domingo"
    valverde = "valverde"


class Hospital(Base):
    __tablename__ = "hospital"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    schedule = Column(String(250))
    location_id = Column(Integer, ForeignKey("location.id"))
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime)

    location = relationship(
        "Location",
        backref=backref("location", uselist=False),
        lazy="joined",
        join_depth=2
    )


class Doctor(Base):
    __tablename__ = "doctor"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    hospital_id = Column(Integer, ForeignKey("hospital.id"))
    schedule = Column(String(250))

    specialties = relationship(
        "Specialty",
        secondary=doctor_to_specialty_association,
        back_populates="doctors"
    )
    user = relationship(
        "User",
        uselist=False,
        lazy="joined",
        join_depth=2
    )
    checkups = relationship("Checkup")


class Specialty(Base):
    __tablename__ = "specialty"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    hospital_id = Column(Integer, ForeignKey("hospital.id"))

    doctors = relationship(
        "Doctor",
        secondary=doctor_to_specialty_association,
        back_populates="specialties"
    )


class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    address = Column(String(length=250))
    province = Column(Enum(Province))


class BloodType(str, enum.Enum):
    a_plus = "a_plus"
    a_minus = "a_minus"
    b_plus = "b_plus"
    b_minus = "b_minus"
    o_plus = "o_plus"
    o_minus = "o_minus"
    ab_plus = "ab_plus"
    ab_minus = "ab_minus"


class Template(Base):
    __tablename__ = "template"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    specialty_id = Column(Integer, ForeignKey("specialty.id"))
    hospital_id = Column(Integer, ForeignKey("hospital.id"))
    headers = Column(JSON)
    numeric_fields = Column(Integer)
    alphanumeric_fields = Column(Integer)
    file_upload_fields = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime)


class UserRole(str, enum.Enum):
    admin = "admin"
    doctor = "doctor"
    patient = "patient"


class DocumentType(str, enum.Enum):
    national_id = "national_id"
    passport = "passport"


class Patient(Base):
    __tablename__ = "patient"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    blood_type = Column(Enum(BloodType))
    medical_background = Column(String)

    user = relationship(
        "User",
        back_populates="patient",
        lazy="joined",
        join_depth=2
    )

    checkups = relationship("Checkup")


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
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    patient = relationship("Patient", back_populates="user", uselist=False)
    doctor = relationship("Doctor", back_populates="user", uselist=False)
    admin = relationship("Admin", back_populates="user", uselist=False)


engine = start_engine()

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"


def create_tables():
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
