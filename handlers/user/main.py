from aiogram import Dispatcher
from aiogram.types import Message
from loguru import logger

from config import connectToDB, CHANNEL_LINK
from handlers.msg_text import MAIN_MENU_TEXT
from handlers.keyboards import *
from handlers.user.register import _register_register_handlers
from handlers.user.user_help import _register_help_handlers


async def __sub_succeed():
    pass


def register_users_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(__sub_succeed, lambda c: c.data == 'check_sub')

    _register_register_handlers(dp)
    _register_help_handlers(dp)
