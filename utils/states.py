from typing import Final
from aiogram.dispatcher.filters.state import StatesGroup, State


class ADPosting(StatesGroup):
    WriteText: Final = State()
    CheckPost: Final = State()
    SendPost: Final = State()