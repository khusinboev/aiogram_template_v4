from datetime import datetime
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from bot.database.models import User, UserInteraction


class UserRepository:
    """Repository for User operations"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Get user by telegram ID"""
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()
    
    async def create(self, telegram_id: int, **kwargs) -> User:
        """Create new user"""
        user = User(telegram_id=telegram_id, **kwargs)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def update_last_interaction(self, telegram_id: int) -> None:
        """Update user's last interaction time"""
        await self.session.execute(
            update(User)
            .where(User.telegram_id == telegram_id)
            .values(last_interaction=datetime.utcnow())
        )
        await self.session.commit()
    
    async def increment_messages(self, telegram_id: int) -> None:
        """Increment user's message count"""
        await self.session.execute(
            update(User)
            .where(User.telegram_id == telegram_id)
            .values(total_messages=User.total_messages + 1)
        )
        await self.session.commit()
    
    async def track_interaction(
        self, 
        telegram_id: int, 
        interaction_type: str, 
        content: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> None:
        """Track user interaction"""
        interaction = UserInteraction(
            user_id=telegram_id,
            interaction_type=interaction_type,
            content=content,
            metadata=metadata or {}
        )
        self.session.add(interaction)
        await self.session.commit()
    
    async def get_total_users(self) -> int:
        """Get total number of users"""
        result = await self.session.execute(select(func.count(User.id)))
        return result.scalar_one()
    
    async def get_active_users(self, days: int = 7) -> int:
        """Get number of active users in last N days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        result = await self.session.execute(
            select(func.count(User.id))
            .where(User.last_interaction >= cutoff_date)
        )
        return result.scalar_one()


from datetime import timedelta