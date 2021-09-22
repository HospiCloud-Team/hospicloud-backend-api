import datetime
from typing import Optional
from enum import Enum

from pydantic import BaseModel, EmailStr


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
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
