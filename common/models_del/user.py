import enum
from .base import Base
from .doctor import Doctor
from .patient import Patient
from .admin import Admin
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Enum, Date, DateTime


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
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    patient = relationship("Patient", back_populates="user", uselist=False)
    doctor = relationship("Doctor", back_populates="user", uselist=False)
    admin = relationship("Admin", back_populates="user", uselist=False)
