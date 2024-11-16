from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.token import Token
from datetime import datetime

# Store a token in the database
async def store_token(token_str: str, user_id: int, expiration: datetime, session: AsyncSession):
    token = Token(token=token_str, user_id=user_id, expiration=expiration)
    session.add(token)
    await session.commit()

# Mark token as revoked
async def revoke_token(token_str: str, session: AsyncSession):
    statement = select(Token).where(Token.token == token_str)
    result = await session.execute(statement)
    token = result.scalar_one_or_none()
    
    if token:
        token.revoked = True
        await session.commit()

# Check if a token is revoked
async def is_token_revoked(token_str: str, session: AsyncSession) -> bool:
    statement = select(Token).where(Token.token == token_str)
    result = await session.execute(statement)
    token = result.scalar_one_or_none()
    
    if token:
        return token.revoked
    return False
