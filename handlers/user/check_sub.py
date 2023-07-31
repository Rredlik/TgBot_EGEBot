import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import CHANNEL_LINK
from database.methods import user_stage
from filters.main import IsSubscriber
from handlers.keyboards import kb_main
from utils.states import Register


async def __sub_unsucceed(query: CallbackQuery):
    # markup = InlineKeyboardMarkup() \
    #     .add(InlineKeyboardButton('✅ Проверить подписку', callback_data='check_sub_second')) \
    #     .add(InlineKeyboardButton('👩🏼‍💻 Тех. поддержка', url='t.me/skidikis'))
    # await query.bot.send_message(query.from_user.id,
    #                              'К сожалению, не вижу твоей подписки. Давай попробуем ещё раз.\n\n'
    #                              f'📚Чтобы начать обучение, подпишись на наш канал {CHANNEL_LINK}\n\n'
    #                              'P.s. Если у тебя возникла проблема с подпиской - напиши в тех. поддержку',
    #                              reply_markup=markup)
    pass


async def __sub_succeed(query: CallbackQuery):

    # await Register.SucceedSub.set()
    userStage = await user_stage.get(query.from_user.id)
    if userStage == 1:
        msgText = ('👍 Отлично! Вижу твою подписку.\n\n'
                   '🚀 Не теряй времени - давай начнем это увлекательное путешествие '
                   'в мир Python вместе!')
        btnText = "Начинаем!"
    else:
        msgText = ('👍 Отлично! Вижу твою подписку.\n\n'
                   '🚀 Не теряй времени - давай продолжим это увлекательное путешествие '
                   'в мир Python вместе!')
        btnText = "Продолжаем!"
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton(btnText, callback_data='sub_succeed_cont'))
    await query.bot.send_message(query.from_user.id,
                                 msgText,
                                 reply_markup=markup)


async def __mainMenu(query: CallbackQuery, state: FSMContext):
    await state.reset_state()
    await query.bot.send_photo(query.from_user.id, photo='AgACAgIAAxkBAAIMI2S_q3S_Q29ZX_1911gz9NWOw'
                                                         'XuiAAIfzjEbyZL4SRtXboqJqfD6AQADAgADdwADLwQ')
    await query.bot.send_document(chat_id=query.from_user.id,
                                  document='BQACAgIAAxkBAAINP2TCEf0Wrr0f-RLQLI0K7cM0OBYNAAJ7MwACQM4RSoLpdf5X1qH9LwQ')
    await asyncio.sleep(0.5)
    await query.bot.send_message(query.from_user.id,
                                 '🚀Для того, чтобы приступить к обучению, перейди в главное меню и нажми кнопку '
                                 '«Модуль 1»\n\n '
                                 'P.s. Если кнопки скрыты - нажми на иконку 🎛 в правом нижнем углу рядом с микрофоном',
                                 reply_markup=await kb_main())


# async def __instruction(query: CallbackQuery):
#     await query.bot.send_message(query.from_user.id,
#                                  '🚀Для того, чтобы приступить к обучению, перейди в главное меню и нажми кнопку '
#                                  '«Модуль 1»\n\n '
#                                  'P.s. Если кнопки скрыты - нажми на иконку 🎛 в правом нижнем у
#                                  глу рядом с микрофоном',
#                                  reply_markup=await kb_main())


def _register_usersReg_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(__sub_succeed, lambda c: c.data == 'check_sub' or c.data == 'check_sub_second',
                                       IsSubscriber(), state='*')
    dp.register_callback_query_handler(__sub_unsucceed, lambda c: c.data == 'check_sub' or c.data == 'check_sub_second',
                                       IsSubscriber(), state='*')

    dp.register_callback_query_handler(__mainMenu, lambda c: c.data == 'sub_succeed_cont', IsSubscriber(),
                                       state=Register.SucceedSub)

    # dp.register_callback_query_handler(__instruction, lambda c: c.data == 'instruction')
