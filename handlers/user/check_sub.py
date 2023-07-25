from aiogram import Dispatcher
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from filters.main import IsSubscriber
from handlers.keyboards import sub_succeed_cont, check_sub_second, to_instruction, kb_main
from handlers.user.register import _register_register_handlers
from handlers.user.user_help import _register_help_handlers


async def __sub_unsucceed(query: CallbackQuery):
    await query.bot.send_message(query.from_user.id,
                                 'К сожалению, не вижу твоей подписки. Давай попробуем ещё раз.\n\n'
                                 'Если возникают какие-то вопросы/проблемы с подпиской - можешь написать нашему '
                                 'менеджеру',
                                 reply_markup=await check_sub_second())


async def __sub_succeed(query: CallbackQuery):
    await query.bot.send_message(query.from_user.id,
                                 'Отлично! Вижу твою подписку.\n'
                                 'Ну что, готов начать обучаться вместе?',
                                 reply_markup=await sub_succeed_cont())


async def __mainMenu(query: CallbackQuery):
    await query.bot.send_photo(query.from_user.id, photo='media/start_photo.jpg',
                               caption='краткое описание всех модулей (т.е. текстовый блок)',
                               reply_markup=await to_instruction())


async def __instruction(query: CallbackQuery):
    await query.bot.send_message(query.from_user.id,
                                 'Для того, чтобы приступить к обучению, перейди в главное меню и нажми кнопку '
                                 '«Модуль 1»\n\n'
                                 'По мере выхода уроков мы будем добавлять новые кнопки и сообщать тебе об этом',
                                 reply_markup=await kb_main())


def _register_usersReg_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(__sub_succeed, lambda c: c.data == 'check_sub' or c.data == 'check_sub_second',
                                       IsSubscriber())
    dp.register_callback_query_handler(__sub_unsucceed, lambda c: c.data == 'check_sub' or c.data == 'check_sub_second')

    dp.register_callback_query_handler(__mainMenu, lambda c: c.data == 'sub_succeed_cont')

    dp.register_callback_query_handler(__mainMenu, lambda c: c.data == 'sub_succeed_cont')
