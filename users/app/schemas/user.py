import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, constr
from common.models import UserRole, DocumentType


class UserBase(BaseModel):
    user_role: UserRole
    document_type: DocumentType
    name: str
    last_name: str
    email: EmailStr
    document_number: constr(max_length=11)
    date_of_birth: datetime.date
    created_at = datetime.datetime.now()
    updated_at: Optional[datetime.datetime] = None


class UserIn(UserBase):
    password: str


class User(UserBase):
    id: int
    created_by: int
    update_by: int

    class Config:
        orm_mode = True
