from datetime import timezone, timedelta
from pathlib import Path
import sys

from pydantic_settings import BaseSettings, SettingsConfigDict


DEBUG = True

TIMEZONE: timezone = timezone.utc

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Env(BaseSettings):
    # ---------------------------------------------
    # Postgresql
    # ---------------------------------------------

    POSTGRESQL_USER: str
    POSTGRESQL_PASSWORD: str
    POSTGRESQL_HOST: str
    POSTGRESQL_PORT: int
    POSTGRESQL_DATABASE: str

    # ---------------------------------------------
    # Jwt authentication
    # ---------------------------------------------

    JWT_ALGORITHM: str
    JWT_TOKEN: str
    JWT_ISS: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env"
    )


env = Env()


ASYNC_DATABASE_URL = f"postgresql+asyncpg://{env.POSTGRESQL_USER}:{env.POSTGRESQL_PASSWORD}@{env.POSTGRESQL_HOST}:{env.POSTGRESQL_PORT}/{env.POSTGRESQL_DATABASE}"
SYNC_DATABASE_URL = f"postgresql+psycopg2://{env.POSTGRESQL_USER}:{env.POSTGRESQL_PASSWORD}@{env.POSTGRESQL_HOST}:{env.POSTGRESQL_PORT}/{env.POSTGRESQL_DATABASE}"


# ------------------------
# Logging Configuration
# ------------------------

# Logging settings for development/debug mode
LOG_DEBUG_SETTINGS = [
    {
        "sink": sys.stdout,
        "format": "<green>{time: YYYY:MM:DD HH:mm:ss}</green> | <level>{level: <8}</level> | "
                  "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>",
        "colorize": True,
        "level": "DEBUG",
    },
    {
        "sink": BASE_DIR / "logs/debug.log",
        "level": "INFO",
        "format": "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        "rotation": "7 days",   # Create a new log file every 7 days
        "retention": "1 month", # Keep logs for one month before deletion
        "compression": "zip",   # Compress logs after rotation
    }
]

# Logging settings for production mode
LOG_PRODUCTION_SETTINGS = [
    {
        "sink": BASE_DIR / "logs/app.log",
        "level": "INFO",
        "format": "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        "rotation": "7 days",
        "retention": "1 month",
        "compression": "zip",
        "enqueue": True
    }
]


JWT_TOKEN = env.JWT_TOKEN
JWT_ALGORITHM = env.JWT_ALGORITHM
JWT_EXP = timedelta(minutes=15)
JWT_ISS = env.JWT_ISS
