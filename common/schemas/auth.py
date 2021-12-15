from pydantic import BaseModel, EmailStr
from .user import UserRole


class FirebaseUser(BaseModel):
    hospital_id: int
    user_role: UserRole
    email: EmailStr
    uid: str
