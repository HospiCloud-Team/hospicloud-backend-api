import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, EmailStr

from schemas.patient import PatientIn, Patient
from schemas.admin import Admin, AdminBase


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


class User(UserBase):
    id: int
    patient: Optional[Patient] = None
    admin: Optional[Admin] = None

    class Config:
        orm_mode = True