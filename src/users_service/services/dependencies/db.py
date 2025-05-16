from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from src.users_service.infrastructure.db.setup import session_factory


async def session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session


async def transaction() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as transaction:
        yield transaction
