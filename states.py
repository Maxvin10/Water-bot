from aiogram.fsm.state import State, StatesGroup

class sign(StatesGroup):
    name = State()
    lastname = State()
    age = State()
    location = State()
    contact = State()
    