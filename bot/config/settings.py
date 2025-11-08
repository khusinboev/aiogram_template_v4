from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""

    # Bot Configuration
    BOT_TOKEN: str = Field(..., description="Telegram Bot Token")
    ADMIN_USER_ID: int = Field(..., description="Main Admin User ID")

    # Database
    USE_SQLITE: bool = Field(default=False, description="Use SQLite instead of PostgreSQL")
    POSTGRES_USER: str = Field(default="botuser")
    POSTGRES_PASSWORD: str = Field(default="botpassword")
    POSTGRES_DB: str = Field(default="telegram_bot")
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: int = Field(default=5432)

    @property
    def DATABASE_URL(self) -> str:
        if self.USE_SQLITE:
            return "sqlite+aiosqlite:///./bot.db"
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # Redis
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    REDIS_DB: int = Field(default=0)

    # AI Integration
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API Key (optional)")

    # Environment
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=True)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


# Try to load settings
try:
    settings = Settings()
    print(f"✅ Settings loaded successfully")
    print(f"   Database: {'SQLite' if settings.USE_SQLITE else 'PostgreSQL'}")
except Exception as e:
    print(f"\n❌ Error loading settings from .env file!")
    print(f"   Error: {e}\n")
    print("💡 Please create .env file in the project root with:")
    print("   BOT_TOKEN=your_bot_token_from_botfather")
    print("   ADMIN_USER_ID=your_telegram_id")
    print("   USE_SQLITE=True\n")
    raise