from typing import Optional
from pydantic import BaseModel, EmailStr
from .user import UserRole


class FirebaseUser(BaseModel):
    hospital_id: Optional[int] = None
    user_role: UserRole
    email: EmailStr
    uid: str
