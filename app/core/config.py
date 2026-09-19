from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict 

class Settings(BaseSettings):
    APP_NAME: str ="Sales Agent"
    DEBUG: bool = False 
    
    model_config = SettingsConfigDict(
        env_file= ".env",
        env_file_encoding ="utf-8",
        extra= "ignore"

    )
    
    

@lru_cache
def get_settings():
    
    return Settings()
    