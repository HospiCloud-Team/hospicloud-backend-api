from enum import Enum
from typing import Optional

from pydantic import BaseModel

from schemas.user import UserIn, User


class BloodType(str, Enum):
    a_plus = "a_plus"
    a_minus = "a_minus"
    b_plus = "b_plus"
    b_minus = "b_minus"
    o_plus = "o_plus"
    o_minus = "o_minus"
    ab_plus = "ab_plus"
    ab_minus = "ab_minus"


class PatientBase(BaseModel):
    blood_type: BloodType
    medical_background: Optional[str] = None


class PatientIn(PatientBase):
    user: UserIn


class Patient(PatientBase):
    id: int
    user: User

    class Config:
        orm_mode = True
