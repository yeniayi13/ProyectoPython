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
    PRODUCT_CAN_BE_ADDED_ROUTE:str
    ORDER_CANCELLED_ROUTE:str
    RMQURL:str


    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=True
    )



@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings