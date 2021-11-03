from .base import Base
from .links import doctor_to_specialty_association
from .doctor import Doctor
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String


class Specialty(Base):
    __tablename__ = "specialty"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    hospital_id = Column(Integer, ForeignKey("hospital.id"))

    doctors = relationship(
        "Doctor",
        secondary=doctor_to_specialty_association,
        back_populates="specialties",
    )
