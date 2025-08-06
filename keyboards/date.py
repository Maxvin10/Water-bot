from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def date(month: str, day: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="-", callback_data="month_minus"),
            InlineKeyboardButton(text=f"{month}", callback_data="month_none"),
            InlineKeyboardButton(text="+", callback_data="month_plus")
        ],
        [
            InlineKeyboardButton(text="-", callback_data="day_minus"),
            InlineKeyboardButton(text=f"{day}", callback_data="day_none"),
            InlineKeyboardButton(text="+", callback_data="day_plus")
        ],
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirm_date")
        ]
    ])
