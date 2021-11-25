from typing import Optional, List
from pydantic import BaseModel

from .specialty import Specialty


class DoctorBase(BaseModel):
    hospital_id: int
    schedule: str


class DoctorIn(DoctorBase):
    specialties: List[int] = []


class DoctorUpdate(BaseModel):
    schedule: Optional[str] = None
    specialties: Optional[List[int]] = None


class Doctor(DoctorBase):
    id: int
    specialties: List[Specialty]

    class Config:
        orm_mode = True
