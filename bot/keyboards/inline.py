from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List
from bot.database.models import Channel


def get_subscription_keyboard(channels: List[Channel]) -> InlineKeyboardMarkup:
    """Create keyboard with subscription channels"""
    buttons = []
    
    for channel in channels:
        # Add channel button
        channel_url = f"https://t.me/{channel.channel_username}" if channel.channel_username else None
        if channel_url:
            buttons.append([
                InlineKeyboardButton(
                    text=f"📢 {channel.channel_title or channel.channel_username}",
                    url=channel_url
                )
            ])
    
    # Add check button
    buttons.append([
        InlineKeyboardButton(
            text="✅ Obunani tekshirish",
            callback_data="check_subscription"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)