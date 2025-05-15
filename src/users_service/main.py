from fastapi import FastAPI

from .loader import lifespan


app = FastAPI(lifespan=lifespan)
