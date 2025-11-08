from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""
    
    # Bot Configuration
    BOT_TOKEN: str = Field(..., description="Telegram Bot Token")
    ADMIN_USER_ID: int = Field(..., description="Main Admin User ID")
    
    # Database
    POSTGRES_USER: str = Field(default="botuser")
    POSTGRES_PASSWORD: str = Field(default="botpassword")
    POSTGRES_DB: str = Field(default="telegram_bot")
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: int = Field(default=5432)
    
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    # Redis
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    REDIS_DB: int = Field(default=0)
    
    # AI Integration
    OPENAI_API_KEY: str = Field(default="", description="OpenAI API Key (optional)")
    
    # Environment
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=True)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


settings = Settings()