from .base import Base
from sqlalchemy import Column, Integer, String, Time, Boolean


class Schedule(Base):
    __tablename__ = "schedule"
    id = Column(Integer, primary_key=True)
    start_day = Column(String)
    end_day = Column(String)
    start_time = Column(Time)
    end_time = Column(Time)
    all_day = Column(Boolean, default=False)
