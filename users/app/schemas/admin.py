from pydantic import BaseModel


class AdminBase(BaseModel):
    hospital_id: int


class Admin(AdminBase):
    id: int

    class Config:
        orm_mode = True
