import datetime
from pydantic import BaseModel
from typing import Optional
from .patient import Patient
from .doctor import Doctor


class CheckupBase(BaseModel):
    data: str


class CheckupIn(CheckupBase):
    doctor_id: int
    patient_id: int
    template_id: int


class Checkup(CheckupBase):
    id: int
    patient: Patient
    doctor: Doctor
    date: datetime.datetime

    class Config:
        orm_mode = True