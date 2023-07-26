from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from config import CHANNEL_LINK
from filters.main import IsSubscriber
from handlers.keyboards import sub_succeed_cont, check_sub_second, to_instruction, kb_main


async def __sub_unsucceed(query: CallbackQuery):
    markup = InlineKeyboardMarkup() \
        .add(InlineKeyboardButton('✅ Проверить подписку', callback_data='check_sub_second')) \
        .add(InlineKeyboardButton('👩🏼‍💻 Тех. поддержка', url='t.me/skidikis'))
    await query.bot.send_message(query.from_user.id,
                                 'К сожалению, не вижу твоей подписки. Давай попробуем ещё раз.\n\n'
                                 f'📚Чтобы начать обучение, подпишись на наш канал {CHANNEL_LINK}\n\n'
                                 'P.s. Если у тебя возникла проблема с подпиской - напиши в тех. поддержку',
                                 reply_markup=markup)


async def __sub_succeed(query: CallbackQuery):
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Начинаем!', callback_data='sub_succeed_cont'))
    await query.bot.send_message(query.from_user.id,
                                 '👍 Отлично! Вижу твою подписку.\n\n'
                                 '🚀 Не теряй времени - давай начнем это увлекательное путешествие '
                                 'в мир Python вместе!',
                                 reply_markup=markup)


async def __mainMenu(query: CallbackQuery):
    await query.bot.send_photo(query.from_user.id, photo='AgACAgIAAxkBAAIMI2S_q3S_Q29ZX_1911gz9NWOw'
                                                         'XuiAAIfzjEbyZL4SRtXboqJqfD6AQADAgADdwADLwQ')
    await query.bot.send_document(query.from_user.id,
                                  ('Учебный план.pdf', 'AgACAgIAAxkBAAIMI2S_q3S_Q29ZX_1911gz9NWOw'
                                                             'XuiAAIfzjEbyZL4SRtXboqJqfD6AQADAgADdwADLwQ'))
    await query.bot.send_message(query.from_user.id,
                                 '🚀Для того, чтобы приступить к обучению, перейди в главное меню и нажми кнопку '
                                 '«Модуль 1»\n\n '
                                 'P.s. Если кнопки скрыты - нажми на иконку 🎛 в правом нижнем углу рядом с микрофоном',
                                 reply_markup=await kb_main())


# async def __instruction(query: CallbackQuery):
#     await query.bot.send_message(query.from_user.id,
#                                  '🚀Для того, чтобы приступить к обучению, перейди в главное меню и нажми кнопку '
#                                  '«Модуль 1»\n\n '
#                                  'P.s. Если кнопки скрыты - нажми на иконку 🎛 в правом нижнем углу рядом с микрофоном',
#                                  reply_markup=await kb_main())


def _register_usersReg_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(__sub_succeed, lambda c: c.data == 'check_sub' or c.data == 'check_sub_second',
                                       IsSubscriber())
    dp.register_callback_query_handler(__sub_unsucceed, lambda c: c.data == 'check_sub' or c.data == 'check_sub_second')

    dp.register_callback_query_handler(__mainMenu, lambda c: c.data == 'sub_succeed_cont')

    # dp.register_callback_query_handler(__instruction, lambda c: c.data == 'instruction')