from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from handlers.msg_text import MAIN_MENU_TEXT
from handlers.keyboards import kb_main
from utils.misc.scheduler_jobs import updateLastMsgTime


async def send_mess_or_cb(msg=None, query=None,
                          message_text=None, markup=None, image=None, video=None, state=None):
    bot, chat_id, message_id = await extractData(msg, query, state)

    if image is None and video is None:
        msgInfo = await bot.send_message(chat_id=chat_id,
                                         text=message_text,
                                         parse_mode='html',
                                         reply_markup=markup)

    else:
        try:

            if image is not None:
                msgInfo = await bot.send_photo(chat_id=chat_id,
                                               photo=image,
                                               caption=message_text,
                                               parse_mode='html',
                                               reply_markup=markup)
            else:
                msgInfo = await bot.send_video(chat_id=chat_id,
                                               video=video,
                                               caption=message_text,
                                               parse_mode='html',
                                               reply_markup=markup)
        except Exception as er:
            logger.error(er)
            msgInfo = await bot.send_message(chat_id=chat_id,
                                             text=message_text,
                                             parse_mode='html',
                                             reply_markup=markup)

    async with state.proxy() as data:
        data['messageId'] = msgInfo.message_id
    await updateLastMsgTime(chat_id)
    return msgInfo


async def extractData(msg=None, query=None, state=None):
    if msg is None:
        bot: Bot = query.bot
        chat_id = query.from_user.id
        message_id = query.message.message_id
        await deletePreviousMessage(bot, chat_id, state)
    else:
        bot: Bot = msg.bot
        chat_id = msg.from_user.id
        message_id = msg.message_id
        await deleteMsgWithReplyMarkup(msg, state)

    return bot, chat_id, message_id


async def deleteMsgWithReplyMarkup(msg, state):
    await state.reset_state()
    async with state.proxy() as data:
        data['messageId'] = msg.message_id
    await deletePreviousMessage(msg.bot, msg.from_user.id, state)


async def deletePreviousMessage(bot, chat_id, state):
    try:
        async with state.proxy() as data:
            message_id = data['messageId']
        await bot.delete_message(chat_id=chat_id,
                                 message_id=message_id)
    except Exception as er:
        logger.error(er)


async def __btn_back_main_menu(query: CallbackQuery, state: FSMContext):
    msg_txt = await MAIN_MENU_TEXT()
    await updateLastMsgTime(userId=query.from_user.id, to_delete=True)
    await send_mess_or_cb(query=query, message_text=msg_txt,
                          markup=await kb_main(), state=state)
    # await deletePreviousMessage(query.bot, query.from_user.id, state)


def _register_utils_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(__btn_back_main_menu, lambda c: c.data and c.data.startswith('close_menu_'),
                                       state='*')