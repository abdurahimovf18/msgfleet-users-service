from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import MetaData

from src.users_service.config.settings import ASYNC_DATABASE_URL


engine = create_async_engine(
    ASYNC_DATABASE_URL,
    pool_size=20,
    max_overflow=10, 
    pool_timeout=30,  
    pool_recycle=1800,
)

metadata = MetaData()
session_factory: sessionmaker[AsyncSession] = sessionmaker(bind=engine, class_=AsyncSession)

Base = declarative_base(metadata=metadata)
