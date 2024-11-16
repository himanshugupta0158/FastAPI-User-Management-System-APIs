from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import async_session
from app.middlewares.auth import check_authorization
from app.models.user import User
from app.routers.auth import hash_password
from app.services.auth_service import get_session
from app.services.user_service import create_user, get_user_by_id, get_all_users, update_user, delete_user
from app.schemas.user import UserCreate, UserRead, UserUpdate
from sqlmodel import select

user_router = APIRouter()


# Create a user
@user_router.post("/", response_model=UserRead)
async def create_new_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    # Check if user with the same email already exists
    existing_user = await session.execute(select(User).where(User.email == user.email))
    existing_user = existing_user.scalar_one_or_none()
    
    if existing_user:
        # If user already exists, raise an HTTPException
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )
    
    db_user = await create_user(user, session)
    return UserRead.from_orm(db_user)


# Get all users
@user_router.get("/", response_model=list[UserRead])
async def get_all_users_data(session: AsyncSession = Depends(get_session)):
    users = await get_all_users(session)
    return [UserRead.from_orm(user) for user in users]


# Get a user by ID
@user_router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.from_orm(user)


# Update a user
@user_router.put("/{user_id}", response_model=UserRead, dependencies=[Depends(check_authorization)])
async def update_existing_user(user_id: int, user_update: UserUpdate, session: AsyncSession = Depends(get_session)):
    updated_user = await update_user(user_id, user_update, session)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.from_orm(updated_user)


# Delete a user
@user_router.delete("/{user_id}", response_model=dict, dependencies=[Depends(check_authorization)])
async def delete_existing_user(user_id: int, session: AsyncSession = Depends(get_session)):
    success = await delete_user(user_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}