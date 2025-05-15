from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field

from src.users_service.domain.models import enums


class UserProfile:
    user_id = Annotated[UUID, Field()]
    language = Annotated[enums.UserLanguages, Field(default=enums.UserLanguages.EN)]
    is_active = Annotated[bool, Field(default=True)] 
    is_deleted = Annotated[bool, Field(default=False)] 


class User:
    id = Annotated[UUID, Field()]
    created_at =  Annotated[datetime, Field()]
    updated_at =  Annotated[datetime, Field()]
