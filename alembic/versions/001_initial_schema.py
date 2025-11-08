"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2025-01-08 21:39:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('telegram_id', sa.BigInteger(), unique=True, nullable=False),
        sa.Column('username', sa.String(255), nullable=True),
        sa.Column('first_name', sa.String(255), nullable=True),
        sa.Column('last_name', sa.String(255), nullable=True),
        sa.Column('language_code', sa.String(10), nullable=True),
        sa.Column('is_bot', sa.Boolean(), default=False),
        sa.Column('is_blocked', sa.Boolean(), default=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('last_interaction', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('first_interaction', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('blocked_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('total_messages', sa.Integer(), default=0),
        sa.Column('total_commands', sa.Integer(), default=0),
        sa.Column('total_sessions', sa.Integer(), default=1),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), default={}),
    )
    
    op.create_index('idx_users_telegram_id', 'users', ['telegram_id'])
    op.create_index('idx_users_created_at', 'users', ['created_at'])
    op.create_index('idx_users_last_interaction', 'users', ['last_interaction'])
    op.create_index('idx_users_is_active', 'users', ['is_active'])

    # User interactions table
    op.create_table(
        'user_interactions',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.BigInteger(), sa.ForeignKey('users.telegram_id', ondelete='CASCADE'), nullable=False),
        sa.Column('interaction_type', sa.String(50), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), default={}),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    
    op.create_index('idx_interactions_user_id', 'user_interactions', ['user_id'])
    op.create_index('idx_interactions_created_at', 'user_interactions', ['created_at'])
    op.create_index('idx_interactions_type', 'user_interactions', ['interaction_type'])

    # User sessions table
    op.create_table(
        'user_sessions',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.BigInteger(), sa.ForeignKey('users.telegram_id', ondelete='CASCADE'), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('ended_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('duration_seconds', sa.Integer(), nullable=True),
        sa.Column('actions_count', sa.Integer(), default=0),
        sa.Column('session_data', postgresql.JSONB(astext_type=sa.Text()), default={}),
    )
    
    op.create_index('idx_sessions_user_id', 'user_sessions', ['user_id'])
    op.create_index('idx_sessions_started_at', 'user_sessions', ['started_at'])

    # Channels table
    op.create_table(
        'channels',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('channel_id', sa.BigInteger(), unique=True, nullable=False),
        sa.Column('channel_username', sa.String(255), nullable=True),
        sa.Column('channel_title', sa.String(255), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('priority', sa.Integer(), default=0),
        sa.Column('added_by', sa.BigInteger(), sa.ForeignKey('users.telegram_id'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('total_checks', sa.Integer(), default=0),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), default={}),
    )

    # User subscriptions table
    op.create_table(
        'user_subscriptions',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.BigInteger(), sa.ForeignKey('users.telegram_id', ondelete='CASCADE'), nullable=False),
        sa.Column('channel_id', sa.Integer(), sa.ForeignKey('channels.id', ondelete='CASCADE'), nullable=False),
        sa.Column('is_subscribed', sa.Boolean(), default=False),
        sa.Column('checked_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('subscribed_at', sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint('user_id', 'channel_id', name='uq_user_channel'),
    )
    
    op.create_index('idx_subscriptions_user_id', 'user_subscriptions', ['user_id'])
    op.create_index('idx_subscriptions_channel_id', 'user_subscriptions', ['channel_id'])

    # Broadcasts table
    op.create_table(
        'broadcasts',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('created_by', sa.BigInteger(), sa.ForeignKey('users.telegram_id'), nullable=False),
        sa.Column('message_text', sa.Text(), nullable=True),
        sa.Column('message_type', sa.String(50), default='text'),
        sa.Column('media_file_id', sa.String(255), nullable=True),
        sa.Column('keyboard_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('target_type', sa.String(50), default='all'),
        sa.Column('target_count', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(50), default='draft'),
        sa.Column('scheduled_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('total_sent', sa.Integer(), default=0),
        sa.Column('total_delivered', sa.Integer(), default=0),
        sa.Column('total_failed', sa.Integer(), default=0),
        sa.Column('total_blocked', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), default={}),
    )

    # Broadcast deliveries table
    op.create_table(
        'broadcast_deliveries',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('broadcast_id', sa.Integer(), sa.ForeignKey('broadcasts.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.BigInteger(), sa.ForeignKey('users.telegram_id', ondelete='CASCADE'), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('sent_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    
    op.create_index('idx_deliveries_broadcast_id', 'broadcast_deliveries', ['broadcast_id'])
    op.create_index('idx_deliveries_user_id', 'broadcast_deliveries', ['user_id'])
    op.create_index('idx_deliveries_status', 'broadcast_deliveries', ['status'])

    # Analytics cache table
    op.create_table(
        'analytics_cache',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('metric_name', sa.String(255), unique=True, nullable=False),
        sa.Column('metric_value', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('calculated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
    )
    
    op.create_index('idx_analytics_metric_name', 'analytics_cache', ['metric_name'])
    op.create_index('idx_analytics_expires_at', 'analytics_cache', ['expires_at'])

    # Bot settings table
    op.create_table(
        'bot_settings',
        sa.Column('key', sa.String(255), primary_key=True),
        sa.Column('value', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('updated_by', sa.BigInteger(), sa.ForeignKey('users.telegram_id'), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('bot_settings')
    op.drop_table('analytics_cache')
    op.drop_table('broadcast_deliveries')
    op.drop_table('broadcasts')
    op.drop_table('user_subscriptions')
    op.drop_table('channels')
    op.drop_table('user_sessions')
    op.drop_table('user_interactions')
    op.drop_table('users')