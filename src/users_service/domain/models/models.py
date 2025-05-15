from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.users_service.domain.models import enums


@dataclass
class UserProfile:
    user_id: UUID
    language: enums.UserLanguages = enums.UserLanguages.EN
    is_active: bool = True
    is_deleted: bool = False


@dataclass
class User:
    id: UUID
    created_at: datetime
    updated_at: datetime
