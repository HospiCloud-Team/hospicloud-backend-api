from .base import Base
from sqlalchemy import Column, ForeignKey, Table

doctor_to_specialty_association = Table(
    "doctor_specialty",
    Base.metadata,
    Column("doctor_id", ForeignKey("doctor.id")),
    Column("specialty_id", ForeignKey("specialty.id")),
)