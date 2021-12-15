import os
from fastapi.param_functions import Depends
from fastapi.requests import Request
from fastapi.security import (
    OAuth2PasswordBearer,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from fastapi.openapi.models import OAuthFlowImplicit
from firebase_admin import auth

from common.models import SessionLocal, Session, create_tables
from common.schemas.auth import FirebaseUser


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(TokenBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            TokenBearer, self
        ).__call__(request)
        return credentials.credentials


async def get_current_user(token: str = Depends(TokenBearer())):
    # check the token with firebase auth
    user_dict = auth.verify_id_token(token)
    user = FirebaseUser(**user_dict)
    return user


def get_db():
    create_tables()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
