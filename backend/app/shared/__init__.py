
from functools import lru_cache
from app.shared.shared_config import Settings

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
