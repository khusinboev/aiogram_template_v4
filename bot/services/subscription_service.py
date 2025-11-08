from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Bot
from typing import List
from bot.database.models import Channel
from bot.database.repositories.channel_repository import ChannelRepository


class SubscriptionService:
    """Service for subscription operations"""
    
    def __init__(self, session: AsyncSession, bot: Bot):
        self.session = session
        self.bot = bot
        self.repo = ChannelRepository(session)
    
    async def check_user_subscriptions(self, user_id: int) -> List[Channel]:
        """
        Check if user is subscribed to all required channels
        Returns list of channels user is NOT subscribed to
        """
        channels = await self.repo.get_active_channels()
        not_subscribed = []
        
        for channel in channels:
            try:
                member = await self.bot.get_chat_member(
                    chat_id=channel.channel_id,
                    user_id=user_id
                )
                
                # Check if user is a member
                if member.status in ["left", "kicked"]:
                    not_subscribed.append(channel)
            except Exception:
                # If error, assume not subscribed
                not_subscribed.append(channel)
        
        return not_subscribed