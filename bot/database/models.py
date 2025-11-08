from datetime import datetime
from sqlalchemy import BigInteger, Integer, String, Boolean, Text, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Optional


class Base(DeclarativeBase):
    """Base class for all models"""
    pass


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    username: Mapped[Optional[str]] = mapped_column(String(255))
    first_name: Mapped[Optional[str]] = mapped_column(String(255))
    last_name: Mapped[Optional[str]] = mapped_column(String(255))
    language_code: Mapped[Optional[str]] = mapped_column(String(10))
    is_bot: Mapped[bool] = mapped_column(Boolean, default=False)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
    last_interaction: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
    first_interaction: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    blocked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    total_messages: Mapped[int] = mapped_column(Integer, default=0)
    total_commands: Mapped[int] = mapped_column(Integer, default=0)
    total_sessions: Mapped[int] = mapped_column(Integer, default=1)
    
    metadata: Mapped[dict] = mapped_column(JSON, default={})
    
    # Relationships
    interactions: Mapped[list["UserInteraction"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    sessions: Mapped[list["UserSession"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    subscriptions: Mapped[list["UserSubscription"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class UserInteraction(Base):
    """User interaction tracking"""
    __tablename__ = "user_interactions"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), index=True)
    interaction_type: Mapped[str] = mapped_column(String(50), index=True)
    content: Mapped[Optional[str]] = mapped_column(Text)
    metadata: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="interactions")


class UserSession(Base):
    """User session tracking"""
    __tablename__ = "user_sessions"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    duration_seconds: Mapped[Optional[int]] = mapped_column(Integer)
    actions_count: Mapped[int] = mapped_column(Integer, default=0)
    session_data: Mapped[dict] = mapped_column(JSON, default={})
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="sessions")


class Channel(Base):
    """Channel model for forced subscription"""
    __tablename__ = "channels"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    channel_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    channel_username: Mapped[Optional[str]] = mapped_column(String(255))
    channel_title: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    priority: Mapped[int] = mapped_column(Integer, default=0)
    added_by: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("users.telegram_id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    total_checks: Mapped[int] = mapped_column(Integer, default=0)
    metadata: Mapped[dict] = mapped_column(JSON, default={})
    
    # Relationships
    subscriptions: Mapped[list["UserSubscription"]] = relationship(back_populates="channel", cascade="all, delete-orphan")


class UserSubscription(Base):
    """User subscription tracking"""
    __tablename__ = "user_subscriptions"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), index=True)
    channel_id: Mapped[int] = mapped_column(Integer, ForeignKey("channels.id", ondelete="CASCADE"), index=True)
    is_subscribed: Mapped[bool] = mapped_column(Boolean, default=False)
    checked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    subscribed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="subscriptions")
    channel: Mapped["Channel"] = relationship(back_populates="subscriptions")