from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    hashed_password: str
    is_active: bool = True
    is_admin: bool = False
    is_staff: bool = False

    # Relationship to Token - Users can have many tokens
    tokens: List["Token"] = Relationship(back_populates="user")
