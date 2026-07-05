from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    UPLOAD_IMAGES_PRODUCT: str = "media/uploads/products"
    ALLOWED_EXTENSIONS: list = ["jpg", "jpeg", "png", "webp"]
    ALLOWED_CONTENT_TYPES: list = ["image/jpg", "image/jpeg", "image/png", "image/webp"]
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB

    class Config:
        env_file = ".env"

settings = Settings()