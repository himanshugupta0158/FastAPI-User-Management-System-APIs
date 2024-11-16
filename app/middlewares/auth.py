from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings


# class RoleMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):

#         if request.url.path in ["/docs", "/openapi.json"]:
#             return await call_next(request)

#         authorization = request.headers.get("Authorization")
#         if not authorization:
#             raise HTTPException(
#                 status_code=401, detail="Authorization header missing")

#         auth = HTTPBearer()
#         credentials: HTTPAuthorizationCredentials = await auth(request)
#         token = credentials.credentials
#         try:
#             payload = jwt.decode(token, settings.SECRET_KEY,
#                                  algorithms=[settings.ALGORITHM])
#             request.state.user = payload
#         except JWTError:
#             raise HTTPException(status_code=401, detail="Invalid token")

#         return await call_next(request)



# Dependency to check Authorization header
def check_authorization(request: Request):
    authorization = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")