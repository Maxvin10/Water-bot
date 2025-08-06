from aiogram import types, Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from states import sign
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from keyboards.contact import contact
from keyboards.suv import water
from keyboards.date import date
from models import User
import config 

router = Router()
user_orders = {}
user_date = {}
user_info = {}


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(sign.name)
    await message.answer("Assalomu alaykum hurmatli mijoz biznig botdan foydalanish uchun ma'lumotlaringizni kiriting 🙂\nIsmingizni kiriting: ")

@router.message(sign.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await message.answer("Familiyangizni kiriting: ")
    await state.set_state(sign.lastname)

@router.message(sign.lastname)
async def get_lastname(message: Message, state: FSMContext):
    await state.update_data(lastname = message.text)
    await message.answer("Yoshingizni kiriting: ") 
    await state.set_state(sign.age)

@router.message(sign.age)
async def get_age(message: Message, state: FSMContext):
    await state.update_data(age = message.text)
    await message.answer("Lakatsiyangizni yozib jo'nating quyidagicha:\nNavoiy shahar Mustaqillik mahallasi Nizomiy ko'chasi 20-xonadon") 
    await state.set_state(sign.location)

@router.message(sign.location)
async def get_location(message: Message, state: FSMContext):
    await state.update_data(location = message.text)
    await message.answer("Raqamingizni yuboring ⬇️ knopka orqali:", reply_markup=contact)
    await state.set_state(sign.contact)

@router.message(sign.contact)
async def get_contact(message: Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data(contact=phone_number)
    data = await state.get_data()

    # foydalanuvchi ID bo‘yicha user_info dict'ga yozamiz
    user_id = message.from_user.id
    user_info[user_id] = {
        "name": data.get("name"),
        "lastname": data.get("lastname"),
        "age": data.get("age"),
        "location": data.get("location"),
        "contact": phone_number
    }

    await User.create(**user_info[user_id])

    await message.answer("Ma'lumotlaringiz saqlandi botdan foydalanish uchun /menu buyrug'ini yuboring ✅")
    await state.clear()




@router.message(F.text == "/menu")
async def show_menu(message):
    user_id = message.from_user.id
    user_orders[user_id] = {'5l': 0, '10l': 0, '19l': 0}
    kb = water(user_orders[user_id])
    await message.answer("Qanday suv buyurtma qilmoqchisiz 💧 ?", reply_markup=kb)

@router.callback_query(F.data.regexp(r"^(5l|10l|19l)_(plus1|plus5|minus1|minus5)$"))
async def update_quantity(callback: CallbackQuery):
    user_id = callback.from_user.id
    key, action = callback.data.split("_")

    if user_id not in user_orders:
        user_orders[user_id] = {'5l': 0, '10l': 0, '19l': 0}

    amount = user_orders[user_id][key]
    if action == "plus1":
        amount += 1
    elif action == "plus5":
        amount += 5
    elif action == "minus1":
        amount = max(0, amount - 1)
    elif action == "minus5":
        amount = max(0, amount - 5)

    user_orders[user_id][key] = amount

    new_kb = water(user_orders[user_id])
    await callback.message.edit_reply_markup(reply_markup=new_kb)
    await callback.answer()


# oylarni olaman
months = [
    "Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun",
    "Iyul", "Avgust", "Sentyabr", "Oktabr", "Noyabr", "Dekabr"
]

@router.callback_query(F.data == "confirm_order")
async def ask_date(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_date[user_id] = {"month": "Avgust", "day": 6}
    kb = date("Avgust", 6)
    await callback.message.answer("Buyurtmangizni qachon yetkazib berishimiz kerak?", reply_markup=kb)
    await callback.answer()

@router.callback_query(F.data.startswith("month_") | F.data.startswith("day_"))
async def update_date(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = user_date.get(user_id, {"month": "Avgust", "day": 1})

    current_month = user_data["month"]
    current_day = user_data["day"]
    month_index = months.index(current_month)

    
    if callback.data == "month_plus":
        month_index = (month_index + 1) % 12
    elif callback.data == "month_minus":
        month_index = (month_index - 1) % 12
    elif callback.data == "day_plus":
        current_day = min(current_day + 1, 31)
    elif callback.data == "day_minus":
        current_day = max(current_day - 1, 1)

    
    new_month = months[month_index]
    user_date[user_id] = {"month": new_month, "day": current_day}

    
    new_kb = date(new_month, current_day)

    await callback.message.edit_reply_markup(reply_markup=new_kb)
    await callback.answer()


    
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Lokatsiyani yuborish", request_location=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    await callback.answer()


@router.callback_query(F.data == "confirm_date")
async def ask_confirm(callback: CallbackQuery):
    user_id = callback.from_user.id
    date_data = user_date.get(user_id)

    # Sanani eslataman
    await callback.message.answer(f"✅ Sana tanlandi: {date_data['day']} {date_data['month']}")

    # Adminga junatishim kerak
    confirm_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha, buyurtmani yubor", callback_data="final_confirm"),
            InlineKeyboardButton(text="❌ Yo‘q, bekor qilish", callback_data="cancel_order")
        ]
    ])
    await callback.message.answer("Buyurtmani tasdiqlaysizmi?", reply_markup=confirm_kb)
    await callback.answer()


@router.callback_query(F.data == "final_confirm")
async def send_order_to_admin(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    order = user_orders.get(user_id, {})
    date_data = user_date.get(user_id, {})
    user_data = user_info.get(user_id, {})

    # Narxlar
    prices = {
        "5l": 5000,
        "10l": 10000,
        "19l": 15000
    }

    # Hhar bitta litr uchun narxni hisoblab ketaman
    total_price = (
        order.get('5l', 0) * prices['5l'] +
        order.get('10l', 0) * prices['10l'] +
        order.get('19l', 0) * prices['19l']
    )

    text = (
        f"🆕 Yangi buyurtma!\n"
        f"👤 Foydalanuvchi: @{callback.from_user.username}\n"
        f"🧾 Ismi: {user_data.get('name')} {user_data.get('lastname')}, {user_data.get('age')} yosh\n"
        f"📞 Tel: {user_data.get('contact')}\n"
        f"📍 Manzil: {user_data.get('location')}\n"
        f"📦 Buyurtma: 5L - {order.get('5l', 0)} ta, 10L - {order.get('10l', 0)} ta, 19L - {order.get('19l', 0)} ta\n"
        f"📅 Yetkazish Sanasi: {date_data.get('day')} {date_data.get('month')}\n"
        f"💰 Umumiy summa: {total_price:,} so'm"
    )

    await callback.bot.send_message(chat_id=config.ADMIN_ID, text=text)
    await callback.message.answer("✅ Buyurtmangiz adminga yuborildi. Tez orada siz bilan bog‘lanamiz.")
    await callback.answer()

    # Danniylani tozalashim kerak
    user_orders.pop(user_id, None)
    user_date.pop(user_id, None)
    user_info.pop(user_id, None)

    await state.clear()




@router.callback_query(F.data == "cancel_order")
async def cancel_order(callback: CallbackQuery):
    await callback.message.answer("❌ Buyurtma bekor qilindi. Qaytadan boshlash uchun /menu buyrug‘ini yuboring.")
    await callback.answer()





