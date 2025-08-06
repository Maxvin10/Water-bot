from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def water(quantities: dict):
    def row(title, key):
        qty = quantities.get(key, 0)
        return [
            [InlineKeyboardButton(text=f"{title} | {qty} ta", callback_data="ignore")],
            [
                InlineKeyboardButton(text="➖5", callback_data=f"{key}_minus5"),
                InlineKeyboardButton(text="➖1", callback_data=f"{key}_minus1"),
                InlineKeyboardButton(text="➕1", callback_data=f"{key}_plus1"),
                InlineKeyboardButton(text="➕5", callback_data=f"{key}_plus5")
            ]
        ]

    buttons = (
        row("5L", "5l") +
        row("10L", "10l") +
        row("19L", "19l") +
        [[InlineKeyboardButton(text="✅ Buyurtmani tasdiqlash", callback_data="confirm_order")]]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons)
