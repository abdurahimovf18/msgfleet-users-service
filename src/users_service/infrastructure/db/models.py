from typing import Annotated
from functools import partial
from datetime import datetime
from uuid import uuid4, UUID

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, DateTime, text, UUID as SQLUUID

from src.users_service.config.settings import TIMEZONE
from src.users_service.infrastructure.db.setup import Base
from src.users_service.domain.models import enums


id_ = Annotated[UUID, mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=lambda: uuid4())]
created_at = Annotated[datetime, mapped_column(DateTime, server_default=text(f"TIMEZONE('{TIMEZONE!s}', NOW())"))]
updated_at = Annotated[datetime, mapped_column(DateTime, server_default=text(f"TIMEZONE('{TIMEZONE!s}', NOW())"), 
                                               onupdate=partial(datetime.now, TIMEZONE))]


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[id_]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    
    profile: Mapped["UserProfile"] = relationship("UserProfile", back_populates="user", uselist=False)


class UserProfile(Base):
    __tablename__ = "user_profiles"

    user_id: Mapped[id_] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    language: Mapped[enums.UserLanguages] = mapped_column(server_default=enums.UserLanguages.EN)

    user: Mapped["User"] = relationship("User", back_populates="profile")
