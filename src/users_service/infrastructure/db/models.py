from typing import Annotated
from functools import partial
from datetime import datetime
from uuid import uuid4, UUID

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import BigInteger, ForeignKey, DateTime, text, Boolean, UUID as SQLUUID

from src.users_service.config.settings import TIMEZONE
from src.users_service.infrastructure.db.setup import Base
from src.users_service.domain.models import enums


id_ = Annotated[UUID, mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=lambda: uuid4())]
created_at = Annotated[datetime, mapped_column(DateTime, server_default=text(f"TIMEZONE('{TIMEZONE!s}', NOW())"))]
updated_at = Annotated[datetime, mapped_column(DateTime, server_default=text(f"TIMEZONE('{TIMEZONE!s}', NOW())"), 
                                               onupdate=partial(datetime.now, TIMEZONE))]

bigint = Annotated[int, mapped_column(BigInteger)]

tb = Annotated[bool, mapped_column(Boolean, server_default=text("true"))]
fb = Annotated[bool, mapped_column(Boolean, server_default=text("false"))]


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[id_]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    
    auth: Mapped["UserAuth"] = relationship("UserAuth", back_populates="user", uselist=False)
    profile: Mapped["UserProfile"] = relationship("UserProfile", back_populates="user", uselist=False)


class UserAuth(Base):
    __tablename__ = "user_auth"

    user_id: Mapped[id_] = mapped_column(ForeignKey("users.id"), primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    privilage: Mapped[enums.UserPrivileges] = mapped_column(server_default=enums.UserPrivileges.USER.value)

    user: Mapped["User"] = relationship("User", back_populates="auth")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    user_id: Mapped[id_] = mapped_column(ForeignKey("users.id"), primary_key=True)
    language: Mapped[enums.UserLanguages] = mapped_column(server_default=enums.UserLanguages.EN)
    is_active: Mapped[tb]
    is_deleted: Mapped[fb]

    user: Mapped["User"] = relationship("User", back_populates="profile")
