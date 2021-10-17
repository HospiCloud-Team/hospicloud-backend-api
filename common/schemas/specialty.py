from enum import Enum
from typing import Optional
from pydantic import BaseModel


class SpecialtyBase(BaseModel):
    name: str


class SpecialtyIn(SpecialtyBase):
    pass


class Specialty(SpecialtyBase):
    id: int

    class Config:
        orm_mode = True
