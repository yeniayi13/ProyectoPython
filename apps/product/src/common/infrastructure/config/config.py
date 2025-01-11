from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DATABASE: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    PGADMIN_DEFAULT_EMAIL: str
    PGADMIN_DEFAULT_PASSWORD: str
    JWT_SECRET: str = 'mysecret'
    JWT_ALGORITHM: str = "HS256"
    JWT_TEST: str
    PORT: int = 8000
    RABBIT_HOST: str
    RABBIT_USER: str
    RABBIT_PASSWORD: str
    TEST: bool = False

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=True,
    )

@lru_cache
def get_settings() -> Settings:
    try:
        settings = Settings()
        return settings
    except Exception as e:
        print(f"Error al cargar los ajustes: {e}")
        return None