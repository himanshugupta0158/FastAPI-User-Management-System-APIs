from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.db import engine
from sqlalchemy.orm import selectinload

from app.services.auth_service import get_session, hash_password


async def create_user(user_create: UserCreate, session: AsyncSession) -> User:
    # Hash password before saving
    hashed_password = hash_password(user_create.password)
    db_user = User(
        name=user_create.name,
        email=user_create.email,
        hashed_password=hashed_password,
        is_active=True,  # Default value
        is_admin=False,  # Default value
        is_staff=False,  # Default value
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def get_user_by_id(user_id: int, session: AsyncSession) -> User:
    statement = select(User).where(User.id == user_id)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()
    return user


async def get_all_users(session: AsyncSession) -> list[User]:
    statement = select(User)
    result = await session.execute(statement)
    return result.scalars().all()


async def update_user(user_id: int, user_update: UserUpdate, session: AsyncSession) -> User:
    user = await get_user_by_id(user_id, session)
    if not user:
        return None

    if user_update.name:
        user.name = user_update.name
    if user_update.email:
        user.email = user_update.email
    if user_update.password:
        user.hashed_password = hash_password(user_update.password)

    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(user_id: int, session: AsyncSession) -> bool:
    user = await get_user_by_id(user_id, session)
    if not user:
        return False

    await session.delete(user)
    await session.commit()
    return True



# Function to create an admin user without using session
async def create_admin_user(email: str, password: str):
    # Create a direct connection to the database
    async with engine.connect() as conn:
        # Check if the admin user already exists
        result = await conn.execute(select(User).where(User.email == email))
        admin_user = result.scalar_one_or_none()

        if admin_user:
            print("Admin user already exists.")
            return

        # If not, create the admin user
        hashed_password = hash_password(password)
        new_admin_user = User(
            name="Admin",
            email=email,
            hashed_password=hashed_password,
            is_admin=True,  # Mark this user as admin
            is_active=True
        )

        # Insert the new admin user into the database
        await conn.execute(
            User.__table__.insert().values(
                name=new_admin_user.name,
                email=new_admin_user.email,
                hashed_password=new_admin_user.hashed_password,
                is_admin=new_admin_user.is_admin,
                is_active=new_admin_user.is_active
            )
        )
        # Commit the transaction
        await conn.commit()

        print(f"Admin user created with email: {email}")


async def get_user_by_email(email: str, session: AsyncSession) -> User:
    # Get the user by email from the database
    statement = select(User).where(User.email == email)
    result = await session.execute(statement)
    return result.scalar_one_or_none()