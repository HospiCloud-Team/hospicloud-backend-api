import datetime
from .base import Base
from .location import Location
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, ForeignKey, Integer, DateTime, String


class Hospital(Base):
    __tablename__ = "hospital"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    schedule = Column(String(250))
    location_id = Column(Integer, ForeignKey("location.id"))
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime)

    location = relationship(
        "Location",
        backref=backref("location", uselist=False),
        lazy="joined",
        join_depth=2
    )