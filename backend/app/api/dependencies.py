from typing import Generator
from functools import lru_cache

from app.core.config import Settings
from app.db.session import SessionLocal


@lru_cache()
def get_settings():
    return Settings()


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()