from aiogram import Dispatcher
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from filters.main import IsSubscriber
from handlers.keyboards import sub_succeed_cont
from handlers.user.register import _register_register_handlers
from handlers.user.user_help import _register_help_handlers


async def __sub_unsucceed(query: CallbackQuery):
    await query.bot.send_message(query.from_user.id,
                                 'К сожалению, не вижу твоей подписки. Давай попробуем ещё раз.', )


async def __sub_succeed(query: CallbackQuery):
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Да!',
                                                             callback_data='check_sub'))
    await query.bot.send_message(query.from_user.id,
                                 'Отлично! Вижу твою подписку.\n'
                                 'Ну что, готов начать обучаться вместе?',
                                 reply_markup=await sub_succeed_cont())


def register_users_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(__sub_succeed, lambda c: c.data == 'check_sub', IsSubscriber())
    dp.register_callback_query_handler(__sub_unsucceed, lambda c: c.data == 'check_sub')


    dp.register_callback_query_handler(__sub_succeed, lambda c: c.data == 'sub_succeed_cont', IsSubscriber())

    _register_register_handlers(dp)
    _register_help_handlers(dp)
