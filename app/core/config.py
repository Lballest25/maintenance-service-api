from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None
    AWS_REGION: str = "us-east-1"
    AWS_S3_BUCKET: str = "maintenance-images"

    APP_NAME: str = "Maintenance Service API"
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
