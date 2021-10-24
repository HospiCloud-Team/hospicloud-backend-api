from enum import Enum
from typing import Optional, List
from pydantic import BaseModel


class SpecialtyBase(BaseModel):
    name: str


class SpecialtyIn(SpecialtyBase):
    pass


class Specialty(SpecialtyBase):
    id: int
    hospital_ids: Optional[List[int]] = None

    class Config:
        orm_mode = True
