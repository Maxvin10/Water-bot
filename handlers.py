from aiogram import types, Router, F
from aiogram.types import Message
from states import sign
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

router = Router()

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
    await message.answer("Raqamingizni yuboring ⬇️ knopka orqali:") 
    await state.set_state(sign.contact)

@router.message(sign.contact)
async def get_contact(message: Message, state: FSMContext):
    await state.update_data(contact = message.text)
    await message.answer("Joylashuvingizni yuboring ⬇️ lakatsiya:")
    await state.set_state(sign.location)

@router.message(sign.location)
async def get_location(message: Message, state: FSMContext):
    await state.update_data(location = message.text)
    await message.answer("Ma'lumotlaringiz saqlandi ✅\ndavom ettirish uchun /menu buyrug'ini bering!")


