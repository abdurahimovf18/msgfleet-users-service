from sqlalchemy.ext.asyncio import AsyncSession

from .dto import p, r
from src.users_service.services import queries
from src.users_service.utils.session import session


@session
async def create_user(param: p.CreateUserDTO, session: AsyncSession) -> r.CreateUserDTO:
    user = queries.users.create(
        queries.p.users.CreateDTO(), session)
    
    profile = queries.users_profile.create(
        queries.p.users_profile.CreateDTO(user_id=user.id, language=param.language), session)
    
    return r.CreateUserDTO.model_validate(user.model_dump() | profile.model_dump())
