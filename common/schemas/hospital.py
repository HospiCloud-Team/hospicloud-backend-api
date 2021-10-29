import datetime
from pydantic import BaseModel
from typing import Optional

from pydantic.types import constr
from .location import LocationIn, Location


class HospitalBase(BaseModel):
    name: constr(strip_whitespace=True)
    schedule: constr(strip_whitespace=True)
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None


class HospitalIn(HospitalBase):
    location: LocationIn


class HospitalUpdate(BaseModel):
    name: Optional[constr(strip_whitespace=True)] = None
    schedule: Optional[constr(strip_whitespace=True)] = None
    location: Optional[LocationIn] = None


class Hospital(HospitalBase):
    id: int
    location: Location

    class Config:
        orm_mode = True
