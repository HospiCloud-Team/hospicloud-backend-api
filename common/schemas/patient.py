from enum import Enum
from typing import Optional
from pydantic import BaseModel
from common.models import BloodType


class PatientBase(BaseModel):
    id_blood_type: BloodType
    medical_background: Optional[str] = None


class PatientIn(PatientBase):
    pass


class Patient(PatientBase):
    id: int

    class Config:
        orm_mode = True
