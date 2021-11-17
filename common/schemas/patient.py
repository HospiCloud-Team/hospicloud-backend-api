from typing import Optional
from pydantic import BaseModel
from common.models import BloodType


class PatientBase(BaseModel):
    blood_type: BloodType
    medical_background: Optional[str] = None


class PatientIn(PatientBase):
    pass


class PatientUpdate(BaseModel):
    medical_background: Optional[str] = None


class Patient(PatientBase):
    id: int

    class Config:
        orm_mode = True
