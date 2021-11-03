import enum
from .base import Base
from .user import User
from .checkup import Checkup
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Enum


class BloodType(str, enum.Enum):
    a_plus = "a_plus"
    a_minus = "a_minus"
    b_plus = "b_plus"
    b_minus = "b_minus"
    o_plus = "o_plus"
    o_minus = "o_minus"
    ab_plus = "ab_plus"
    ab_minus = "ab_minus"


class Patient(Base):
    __tablename__ = "patient"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    blood_type = Column(Enum(BloodType))
    medical_background = Column(String)

    user = relationship("User", back_populates="patient", lazy="joined", join_depth=2)

    checkups = relationship("Checkup")
