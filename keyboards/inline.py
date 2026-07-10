from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_admin_request_kb(req_id: int) -> InlineKeyboardMarkup:
    """Создает кнопку под конкретной заявкой"""
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Закрыть заявку", callback_data=f"close_{req_id}")]
        ]
    )
    return kb