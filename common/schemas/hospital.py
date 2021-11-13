import datetime
from pydantic import BaseModel
from typing import Optional

from pydantic.types import constr
from .location import LocationIn, Location, LocationUpdate


class HospitalBase(BaseModel):
    name: constr(strip_whitespace=True)
    description: str
    schedule: constr(strip_whitespace=True)
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None


class HospitalIn(HospitalBase):
    location: LocationIn


class HospitalUpdate(BaseModel):
    name: Optional[constr(strip_whitespace=True)] = None
    description: Optional[str] = None
    schedule: Optional[constr(strip_whitespace=True)] = None
    location: Optional[LocationUpdate] = None


class Hospital(HospitalBase):
    id: int
    location: Location

    class Config:
        orm_mode = True
