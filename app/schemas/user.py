from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase (BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    is_staff: bool

    class Config:
        from_attributes = True  # This allows the usage of from_orm


class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]


