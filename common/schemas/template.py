import datetime
from typing import Optional
from pydantic import BaseModel

from .specialty import Specialty


class TemplateBase(BaseModel):
    title: str
    headers: str
    numeric_fields: Optional[int] = None
    alphanumeric_fields: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None


class TemplateIn(TemplateBase):
    specialty_id: int
    hospital_id: int


class Template(TemplateBase):
    id: int
    specialty = Specialty

    class Config:
        orm_mode = True
