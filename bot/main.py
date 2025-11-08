import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from bot.config.settings import settings
from bot.database.session import init_db
from bot.handlers.user import start, common
from bot.middlewares.analytics import AnalyticsMiddleware
from bot.middlewares.subscription import SubscriptionMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Main function to start the bot"""
    
    # Initialize database
    logger.info("Initializing database...")
    await init_db()
    
    # Initialize bot and dispatcher
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    # Register middlewares
    dp.message.middleware(AnalyticsMiddleware())
    dp.message.middleware(SubscriptionMiddleware())
    
    # Register handlers
    dp.include_router(start.router)
    dp.include_router(common.router)
    
    # Start bot
    logger.info("Bot started successfully!")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")