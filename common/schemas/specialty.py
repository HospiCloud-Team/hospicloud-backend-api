from enum import Enum
from typing import Optional, List
from pydantic import BaseModel
from pydantic.types import constr


class SpecialtyBase(BaseModel):
    name: constr(strip_whitespace=True)
    hospital_id: int


class SpecialtyIn(SpecialtyBase):
    pass


class SpecialtyUpdate(BaseModel):
    name: Optional[constr(strip_whitespace=True)] = None


class Specialty(SpecialtyBase):
    id: int

    class Config:
        orm_mode = True
