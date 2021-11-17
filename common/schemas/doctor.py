from typing import Optional, List
from pydantic import BaseModel

from .specialty import Specialty


class DoctorBase(BaseModel):
    hospital_id: int
    schedule: str


class DoctorIn(DoctorBase):
    specialty_ids: List[int] = []


class DoctorUpdate(BaseModel):
    schedule: Optional[str] = None
    specialty_ids: Optional[List[int]] = None


class Doctor(DoctorBase):
    id: int
    specialties: List[Specialty]

    class Config:
        orm_mode = True
