from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache



class Settings(BaseSettings):
    JWT_SECRET:str
    JWT_ALGORITHM:str
    POSTGRES_USER:str
    PASSWORD:str
    HOST:str
    PORT:str
    DATABASE:str
    RABBIT_HOST: str
    RABBIT_USER: str
    RABBIT_PASSWORD: str
    CLIENT_CREATED_QUEUE:str
    MANAGER_CREATED_QUEUE:str
    SUPERADMIN_CREATED_QUEUE:str
    CLIENT_MODIFIED_QUEUE:str
    MANAGER_MODIFIED_QUEUE:str


    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=True
    )



@lru_cache
def get_settings_auth() -> Settings:
    settings = Settings()
    return settings