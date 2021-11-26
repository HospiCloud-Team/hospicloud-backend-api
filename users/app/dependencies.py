import os
from fastapi_cloudauth.firebase import FirebaseCurrentUser
from fastapi.security import OAuth2PasswordBearer
from common.models import SessionLocal, Session, create_tables
from firebase_admin import auth

def _parse_token(token: str):
    pass

def get_current_user():
    async def get_current_user(token: str = Depends(parse_token)):
    # check the token with firebase auth
    user = auth.verify_id_token(token)
    return user

def get_db():
    create_tables()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
