from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

contact = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text = "📞 Nomer ulashish", request_contact=True)
        ]
    ],
    resize_keyboard= True,
    one_time_keyboard=True
)