from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from sqlalchemy.orm import load_only

from src.users_service.infrastructure.db import models
from src.users_service.domain.models import enums

from ..dto import p, r



async def create(param: p.users.CreateDTO, session: AsyncSession) -> r.users.CreateDTO:
    user = models.User()
    session.add(user)
    await session.flush(user)
    return r.users.CreateDTO.model_validate(user)
