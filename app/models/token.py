from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class Token(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    token: str
    user_id: int = Field(foreign_key="user.id")
    expiration: datetime
    revoked: bool = Field(default=False)
    
    # Back reference to the user
    user: "User" = Relationship(back_populates="tokens")
