from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_USER: str = "root"
    DB_PASSWORD: str = "134679"
    DB_NAME: str = "sample"
    DB_CHARSET: str = "utf8mb4"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
