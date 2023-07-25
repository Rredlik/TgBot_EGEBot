from aiogram import Dispatcher

from handlers.user.check_sub import _register_usersReg_handlers
from handlers.user.register import _register_register_handlers
from handlers.user.user_help import _register_help_handlers


def register_users_handlers(dp: Dispatcher) -> None:
    _register_usersReg_handlers(dp)
    _register_register_handlers(dp)
    _register_help_handlers(dp)
