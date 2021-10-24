from enum import Enum
from typing import Optional, List
from pydantic import BaseModel


class SpecialtyBase(BaseModel):
    name: str
    hospital_id: int


class SpecialtyIn(SpecialtyBase):
    pass


class SpecialtyUpdate(BaseModel):
    name: str


class Specialty(SpecialtyBase):
    id: int

    class Config:
        orm_mode = True
