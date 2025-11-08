"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2025-01-08 21:39:00.000000

"""
from alembic import op
import sqlalchemy as sa

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
        sa.Column('metadata', sa.Text(), default='{}'),  # Text instead of JSONB
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
        sa.Column('metadata', sa.Text(), default='{}'),
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
        sa.Column('session_data', sa.Text(), default='{}'),
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
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('total_checks', sa.Integer(), default=0),
        sa.Column('metadata', sa.Text(), default='{}'),
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
    )

    op.create_index('idx_subscriptions_user_id', 'user_subscriptions', ['user_id'])
    op.create_index('idx_subscriptions_channel_id', 'user_subscriptions', ['channel_id'])


def downgrade() -> None:
    op.drop_table('user_subscriptions')
    op.drop_table('channels')
    op.drop_table('user_sessions')
    op.drop_table('user_interactions')
    op.drop_table('users')