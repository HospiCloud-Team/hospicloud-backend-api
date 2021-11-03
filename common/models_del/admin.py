from .base import Base
from .user import User
from .hospital import Hospital
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer


class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    hospital_id = Column(Integer, ForeignKey("hospital.id"))

    hospital = relationship("Hospital", uselist=False)
    user = relationship("User", uselist=False)
