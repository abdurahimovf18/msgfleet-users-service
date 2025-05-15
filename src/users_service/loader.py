from contextlib import asynccontextmanager
from fastapi import FastAPI

from .infrastructure.logging import set_log
from .api.router import router


set_log()


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    app.include_router(router)

    yield

