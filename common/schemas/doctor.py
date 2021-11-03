from enum import Enum
from typing import Optional
from pydantic import BaseModel
from .specialty import Specialty


class DoctorBase(BaseModel):
    pass


class DoctorIn(DoctorBase):
    id_specialty: int


class Doctor(DoctorBase):
    id: int
    specialty = Specialty

    class Config:
        orm_mode = True
