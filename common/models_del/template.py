import datetime
from .base import Base
from sqlalchemy import Column, ForeignKey, Integer, DateTime, JSON, String


class Template(Base):
    __tablename__ = "template"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    specialty_id = Column(Integer, ForeignKey("specialty.id"))
    hospital_id = Column(Integer, ForeignKey("hospital.id"))
    headers = Column(JSON)
    numeric_fields = Column(Integer)
    alphanumeric_fields = Column(Integer)
    file_upload_fields = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime)
