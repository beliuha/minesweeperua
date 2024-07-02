from aiogram.fsm.state import StatesGroup, State

class Feedback(StatesGroup):
    # Машина станів
    location = State()
    photo = State()
    text = State()
