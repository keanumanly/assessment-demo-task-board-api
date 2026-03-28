from pydantic_settings import BaseSettings, SettingsConfigDict
import redis


class Settings(BaseSettings):
    APP_NAME: str = "Assessment Demo Task Board API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str | None = None
    
    # APIKEY
    APIKEY: str

    # # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"   # ✅ FIX HERE
    )

    @property
    def REDIS_CLIENT(self):
        return redis.Redis(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            db=self.REDIS_DB,
            decode_responses=True
            )


settings = Settings()
