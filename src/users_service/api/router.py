from fastapi import APIRouter, status, HTTPException

from src.users_service.services import flows
from src.users_service.services import queries
from .dto import p, r


router = APIRouter()


@router.post("/create")
async def create(param: p.CreateDTO) -> r.CreateDTO:
    created_user = await flows.create_user(
        flows.p.CreateUserDTO(language=param.language))
    
    return r.CreateDTO.model_validate(created_user.model_dump())
