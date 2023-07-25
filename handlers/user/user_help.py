from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from loguru import logger

from config import VIDEO_INSTRUCTION_ID
from filters.main import NotAdmin
from handlers.msg_text import BTN_CLOSE
from handlers.stuff_methods import deletePreviousMessage, send_mess_or_cb


############### USER HELP ###############

async def __user_help(msg: Message, state: FSMContext):
    userId = msg.from_user.id
    await deletePreviousMessage(msg.bot, userId, state)

    video = VIDEO_INSTRUCTION_ID
    # video = 'BAACAgIAAxkBAAIVHmP946V_jxwEIIY96S8WK_2pc_R7AALTKQACGufoS8HDyOb1O0wYLgQ'
    msgText = 'Инструкция пользователя\n' \
              'Не забудь подписаться на канал'
    markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton('Подписаться', url='https://t.me/isglazkova')).add(await kb_help_user())
    msgInfo = await send_mess_or_cb(msg=msg, message_text=msgText,
                                    video=video, markup=markup, state=state)
    logger.info(f'User_id: {userId}')


async def kb_help_user():
    btn = InlineKeyboardButton(BTN_CLOSE, callback_data='close_menu_')

    return btn


def _register_help_handlers(dp: Dispatcher) -> None:
    # region Msg handlers

    dp.register_message_handler(__user_help, NotAdmin(), Text(equals="📚 Инструкция"), state='*')

    # endregion

    # region Callback handlers

    # dp.register_callback_query_handler(__check_buy, text_contains="check_payment")

    # endregion
