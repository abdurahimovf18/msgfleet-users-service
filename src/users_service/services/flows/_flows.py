from sqlalchemy.ext.asyncio import AsyncSession

from .dto import p, r
from src.users_service.services import queries


async def create_user(param: p.CreateUserDTO, session: AsyncSession) -> r.CreateUserDTO:
    user = await queries.users.create(
        queries.p.users.CreateDTO(), session)
    
    profile = await queries.users_profile.create(
        queries.p.users_profile.CreateDTO(user_id=user.id, language=param.language), session)
    
    await session.commit()

    return r.CreateUserDTO.v(user, profile)
