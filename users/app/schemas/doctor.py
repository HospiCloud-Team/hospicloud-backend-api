from typing import List

from pydantic import BaseModel


class DoctorBase(BaseModel):
    hospital_id: int
    schedule_id: int


class DoctorIn(DoctorBase):
    specialty_ids: List[int] = []


class Doctor(DoctorBase):
    id: int

    class Config:
        orm_mode = True
