from datetime import timedelta, datetime
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import async_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


# Function to verify the JWT token and decode it
def verify_jwt_token(token: str):
    try:
        # Decode the JWT token using the secret key and algorithms
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
