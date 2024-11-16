from fastapi import APIRouter, Depends, HTTPException
from app.schemas.auth import LoginModel, Token
from app.services.auth_service import create_access_token, hash_password, verify_password
from app.services.user_service import get_user_by_email
from app.services.token_service import store_token, revoke_token, is_token_revoked
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import async_session
from datetime import datetime, timedelta
from app.services.auth_service import get_session

auth_router = APIRouter()


# Login route
@auth_router.post("/login", response_model=Token)
async def login(form_data: LoginModel, session: AsyncSession = Depends(get_session)):
    # Fetch the user from the database by email
    user = await get_user_by_email(form_data.email, session)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Validate password
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Create an access token with expiration
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        {"sub": user.email}, expires_delta=expires_delta)
    expiration_time = datetime.utcnow(
    ) + expires_delta

    # Store the token in the database
    await store_token(access_token, user.id, expiration_time, session)

    return {"access_token": access_token, "token_type": "bearer"}


# Logout route
@auth_router.post("/logout")
async def logout(token: str, session: AsyncSession = Depends(get_session)):
    # Revoke the token on logout
    await revoke_token(token, session)
    return {"detail": "Successfully logged out."}


# Protect your routes using a token that is not revoked
@auth_router.get("/protected")
async def protected_route(token: str, session: AsyncSession = Depends(get_session)):
    # Check if the token is revoked
    if await is_token_revoked(token, session):
        raise HTTPException(status_code=401, detail="Token has been revoked")

    return {"message": "This is a protected route"}
