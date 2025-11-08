from datetime import datetime
from sqlalchemy import Column, BigInteger, Integer, String, Boolean, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, relationship
from typing import Optional, List


class Base(DeclarativeBase):
    """Base class for all models"""
    pass


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    language_code = Column(String(10))
    is_bot = Column(Boolean, default=False)
    is_blocked = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    last_interaction = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    first_interaction = Column(DateTime(timezone=True), server_default=func.now())
    blocked_at = Column(DateTime(timezone=True))

    total_messages = Column(Integer, default=0)
    total_commands = Column(Integer, default=0)
    total_sessions = Column(Integer, default=1)

    metadata = Column("metadata", Text, default="{}")

    # Relationships
    interactions = relationship("UserInteraction", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    subscriptions = relationship("UserSubscription", back_populates="user", cascade="all, delete-orphan")


class UserInteraction(Base):
    """User interaction tracking"""
    __tablename__ = "user_interactions"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), index=True)
    interaction_type = Column(String(50), index=True)
    content = Column(Text)
    metadata = Column("metadata", Text, default="{}")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    user = relationship("User", back_populates="interactions")


class UserSession(Base):
    """User session tracking"""
    __tablename__ = "user_sessions"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), index=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    ended_at = Column(DateTime(timezone=True))
    duration_seconds = Column(Integer)
    actions_count = Column(Integer, default=0)
    session_data = Column(Text, default="{}")

    # Relationships
    user = relationship("User", back_populates="sessions")


class Channel(Base):
    """Channel model for forced subscription"""
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True)
    channel_id = Column(BigInteger, unique=True, nullable=False)
    channel_username = Column(String(255))
    channel_title = Column(String(255))
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=0)
    added_by = Column(BigInteger, ForeignKey("users.telegram_id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    total_checks = Column(Integer, default=0)
    metadata = Column("metadata", Text, default="{}")

    # Relationships
    subscriptions = relationship("UserSubscription", back_populates="channel", cascade="all, delete-orphan")


class UserSubscription(Base):
    """User subscription tracking"""
    __tablename__ = "user_subscriptions"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), index=True)
    channel_id = Column(Integer, ForeignKey("channels.id", ondelete="CASCADE"), index=True)
    is_subscribed = Column(Boolean, default=False)
    checked_at = Column(DateTime(timezone=True), server_default=func.now())
    subscribed_at = Column(DateTime(timezone=True))

    # Relationships
    user = relationship("User", back_populates="subscriptions")
    channel = relationship("Channel", back_populates="subscriptions")