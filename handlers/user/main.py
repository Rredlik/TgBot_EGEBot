from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from filters.main import IsSubscriber
from handlers.user.register import _register_register_handlers
from handlers.user.user_help import _register_help_handlers


async def __sub_succeed(query: CallbackQuery):
    await query.bot.send_message(query.from_user.id, 'hi, sub')


async def __sub_unsucceed(query: CallbackQuery):
    await query.bot.send_message(query.from_user.id,
                                 'hi, not sub',)


def register_users_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(__sub_succeed, lambda c: c.data == 'check_sub', IsSubscriber())
    dp.register_callback_query_handler(__sub_unsucceed, lambda c: c.data == 'check_sub')

    _register_register_handlers(dp)
    _register_help_handlers(dp)
