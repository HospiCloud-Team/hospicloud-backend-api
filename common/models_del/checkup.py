import datetime
from .base import Base
from .patient import Patient
from .doctor import Doctor
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, DateTime, JSON


class Checkup(Base):
    __tablename__ = "checkup"
    id = Column(Integer, primary_key=True)
    template_id = Column(Integer, ForeignKey("template.id"))
    doctor_id = Column(Integer, ForeignKey("doctor.id"))
    patient_id = Column(Integer, ForeignKey("patient.id"))
    data = Column(JSON)
    date = Column(DateTime, default=datetime.datetime.now())
    patient = relationship(
        "Patient", back_populates="checkups", lazy="joined", join_depth=2
    )
    doctor = relationship(
        "Doctor", back_populates="checkups", lazy="joined", join_depth=2
    )
