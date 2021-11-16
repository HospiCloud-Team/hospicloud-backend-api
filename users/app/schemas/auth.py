from pydantic import BaseModel
from pydantic.networks import EmailStr

class LogIn(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    token: str