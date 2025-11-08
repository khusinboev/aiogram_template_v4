from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text)
async def handle_text_message(message: Message):
    """Handle any text message from users"""
    await message.answer(
        "📩 Xabaringiz qabul qilindi!\n"
        "Tez orada javob beramiz."
    )