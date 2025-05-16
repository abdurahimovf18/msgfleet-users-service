from fastapi import APIRouter, Depends

from src.users_service.services import flows
from .dto import p, r

from src.users_service.services.dependencies import db


router = APIRouter()


@router.post("/create")
async def create(param: p.CreateDTO,
                 session = Depends(db.session)) -> r.CreateDTO:
    
    created_user = await flows.create_user(
        flows.p.CreateUserDTO(language=param.language), session)
    
    return r.CreateDTO.v(created_user)
