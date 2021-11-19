from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.requests import Request

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(TokenBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            TokenBearer, self
        ).__call__(request)
        return credentials.credentials