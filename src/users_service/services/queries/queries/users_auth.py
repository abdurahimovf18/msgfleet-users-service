from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from sqlalchemy.orm import load_only

from src.users_service.infrastructure.db import models
from src.users_service.domain.models import enums

from ..dto import p, r
