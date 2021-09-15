from pydantic import BaseModel
from common.models import BloodType
from users.app.schemas.user import UserIn


class PatientBase(BaseModel):
    blood_type: BloodType
    medical_background: str

class PatientIn(PatientBase):
    user: UserIn

class Patient(PatientBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True