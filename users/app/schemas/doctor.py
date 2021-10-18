from typing import List, Optional

from pydantic import BaseModel


class DoctorBase(BaseModel):
    hospital_id: int
    schedule_id: int


class DoctorIn(DoctorBase):
    specialty_ids: List[int] = []


class DoctorUpdate(BaseModel):
    schedule_id: Optional[int] = None
    specialty_ids: Optional[List[int]] = None


class Doctor(DoctorBase):
    id: int

    class Config:
        orm_mode = True
