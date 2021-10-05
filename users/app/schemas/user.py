import datetime
from typing import Optional
from enum import Enum

from pydantic import BaseModel, EmailStr

from schemas.patient import PatientIn, Patient, PatientUpdate
from schemas.admin import Admin, AdminBase
from schemas.doctor import Doctor, DoctorIn, DoctorUpdate


class UserRole(str, Enum):
    admin = "admin"
    doctor = "doctor"
    patient = "patient"


class DocumentType(str, Enum):
    national_id = "national_id"
    passport = "passport"


class UserBase(BaseModel):
    user_role: UserRole
    document_type: DocumentType
    name: str
    last_name: str
    email: EmailStr
    document_number: str
    date_of_birth: datetime.date
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None


class UserIn(UserBase):
    patient: Optional[PatientIn] = None
    admin: Optional[AdminBase] = None
    doctor: Optional[DoctorIn] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    document_number: Optional[str] = None
    date_of_birth: datetime.date

    patient: Optional[PatientUpdate] = None
    doctor: Optional[DoctorUpdate] = None


class User(UserBase):
    id: int
    patient: Optional[Patient] = None
    admin: Optional[Admin] = None
    doctor: Optional[Doctor] = None

    class Config:
        orm_mode = True
