from pydantic import BaseModel


class CheckupBase(BaseModel):
    doctor_id: int
    patient_id: int
    data: str


class CheckupIn(CheckupBase):
    template_id: int

    class Config:
        orm_mode = True


class Checkup(CheckupBase):
    id: int
    date: str

    class Config:
        orm_mode = True
