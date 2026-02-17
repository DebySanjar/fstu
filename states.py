from aiogram.fsm.state import State, StatesGroup

class FormStates(StatesGroup):
    """Anketa to'ldirish holatlari"""
    full_name = State()
    faculty = State()
    group = State()
    phone = State()
    logo = State()

class AdminStates(StatesGroup):
    """Admin holatlari"""
    vacancy_text = State()
    search_query = State()

class ContactStates(StatesGroup):
    """Adminga murojaat holatlari"""
    message = State()

class ReplyStates(StatesGroup):
    """Admin javob berish holatlari"""
    user_id = State()
    message = State()
