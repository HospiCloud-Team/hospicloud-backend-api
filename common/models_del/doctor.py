from .base import Base
from .links import doctor_to_specialty_association
from .specialty import Specialty
from .user import User
from .checkup import Checkup
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String


class Doctor(Base):
    __tablename__ = "doctor"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    hospital_id = Column(Integer, ForeignKey("hospital.id"))
    schedule = Column(String(250))
    schedule_id = Column(Integer, ForeignKey("schedule.id"))

    specialties = relationship(
        "Specialty", secondary=doctor_to_specialty_association, back_populates="doctors"
    )
    user = relationship("User", uselist=False, lazy="joined", join_depth=2)
    checkups = relationship("Checkup")
