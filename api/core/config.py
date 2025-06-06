from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_v1_prefix: str = "/v1"

    class Config:
        env_file = ".env"

settings = Settings()
