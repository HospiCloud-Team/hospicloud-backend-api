from typing import Optional

from pydantic import BaseModel

from common.models import BloodType
from schemas.user import UserIn


class PatientBase(BaseModel):
    blood_type: BloodType
    medical_background: Optional[str] = None


class PatientIn(PatientBase):
    user: UserIn


class Patient(PatientBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
