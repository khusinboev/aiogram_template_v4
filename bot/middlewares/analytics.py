from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from bot.database.session import AsyncSessionLocal
from bot.database.repositories.user_repository import UserRepository


class AnalyticsMiddleware(BaseMiddleware):
    """Middleware to track user interactions for analytics"""

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        """Track interaction and call handler"""

        async with AsyncSessionLocal() as session:
            user_repo = UserRepository(session)

            # Update last interaction
            await user_repo.update_last_interaction(event.from_user.id)

            # Increment message count
            await user_repo.increment_messages(event.from_user.id)

            # Track interaction
            interaction_type = "command" if event.text and event.text.startswith("/") else "message"
            await user_repo.track_interaction(
                telegram_id=event.from_user.id,
                interaction_type=interaction_type,
                content=event.text[:500] if event.text else None,  # Limit length
                metadata={
                    "chat_id": event.chat.id,
                    "message_id": event.message_id,
                }
            )

        # Call the handler
        return await handler(event, data)