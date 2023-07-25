from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from handlers.user.check_sub import _register_usersReg_handlers
from handlers.user.open_module import register_openModule_handlers
from handlers.user.register import _register_register_handlers
from handlers.user.user_help import _register_help_handlers


async def __askTp(msg: Message):
    await msg.bot.send_message(chat_id=msg.from_user.id,
                               text='Если у вас возникли вопросы или что-то не работает пишите: @skidikis'
                               )


def register_users_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(__askTp, Text(equals="📚 Тех. поддержка"), state='*')

    _register_usersReg_handlers(dp)
    _register_register_handlers(dp)
    _register_help_handlers(dp)
    register_openModule_handlers(dp)
