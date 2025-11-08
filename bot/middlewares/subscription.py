from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from bot.config.settings import settings
from bot.services.subscription_service import SubscriptionService
from bot.database.session import AsyncSessionLocal
from bot.keyboards.inline import get_subscription_keyboard


class SubscriptionMiddleware(BaseMiddleware):
    """Middleware to check forced subscription"""
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        """Check subscription and call handler"""
        
        # Skip for admin
        if event.from_user.id == settings.ADMIN_USER_ID:
            return await handler(event, data)
        
        # Skip for /start command
        if event.text and event.text == "/start":
            return await handler(event, data)
        
        async with AsyncSessionLocal() as session:
            subscription_service = SubscriptionService(session, event.bot)
            
            # Check if user is subscribed to all required channels
            not_subscribed = await subscription_service.check_user_subscriptions(
                event.from_user.id
            )
            
            if not_subscribed:
                # User is not subscribed to some channels
                keyboard = get_subscription_keyboard(not_subscribed)
                
                await event.answer(
                    "❗️ Botdan foydalanish uchun quyidagi kanallarga obuna bo'lishingiz kerak:",
                    reply_markup=keyboard
                )
                return  # Don't call the handler
        
        # User is subscribed, proceed
        return await handler(event, data)