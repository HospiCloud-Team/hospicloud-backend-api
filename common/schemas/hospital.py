import datetime
from pydantic import BaseModel
from typing import Optional
from .location import LocationIn, Location


class HospitalBase(BaseModel):
    name: str
    schedule: str
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None


class HospitalIn(HospitalBase):
    location: LocationIn


class HospitalUpdate(BaseModel):
    name: Optional[str] = None
    schedule: Optional[str] = None
    location: Optional[LocationIn] = None


class Hospital(HospitalBase):
    id: int
    location: Location

    class Config:
        orm_mode = True
