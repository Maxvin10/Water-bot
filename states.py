from aiogram.fsm.state import State, StatesGroup

class sign(StatesGroup):
    name = State()
    lastname = State()
    age = State()
    contact = State()
    location = State()