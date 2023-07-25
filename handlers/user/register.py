from datetime import datetime

from aiogram import Dispatcher
from aiogram.types import Message, ChatMemberStatus
from loguru import logger

from config import connectToDB, CHANNEL_LINK, CHANNEL_ID
from database.methods import user_stage
from handlers.msg_text import MAIN_MENU_TEXT
from handlers.keyboards import *
from handlers.user.user_help import _register_help_handlers


async def __start(message: Message):
    user_id = message.from_user.id
    is_reg = await is_registered(user_id=user_id)
    msg_txt = await MAIN_MENU_TEXT()
    sub_status = await message.bot.get_chat_member(chat_id=CHANNEL_ID[0], user_id=message.from_user.id)

    if is_reg:

        if not sub_status.status == ChatMemberStatus.LEFT:
            await message.answer(msg_txt,
                                 reply_markup=await kb_main())
        else:
            await message.answer(msg_txt +
                                 f"Подпишись на наш канал {CHANNEL_LINK} и нажимай на кнопку «Подписка есть»",
                                 reply_markup=await check_sub())
    else:
        await message.answer(msg_txt +
                             f"Подпишись на наш канал {CHANNEL_LINK} и нажимай на кнопку «Подписка есть»",
                             reply_markup=await check_sub())



async def is_registered(user_id):
    async with connectToDB() as db:
        try:
            command = await db.execute(
                """SELECT * FROM 'users' WHERE user_id = :user_id""",
                {'user_id': user_id}
            )
            await db.commit()
            values = await command.fetchone()

            if values is None:
                await create_new_user(user_id)
                return False
            else:
                return True
        except Exception as er:
            logger.error(f"{er}")
        finally:
            await db.commit()


async def create_new_user(user_id):
    async with connectToDB() as db:
        try:
            await db.execute(
                "INSERT INTO 'users' (user_id, reg_date) VALUES (?, ?)",
                (user_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            )
            logger.info(f"New user registered: {user_id}")
            await db.commit()
        except Exception as er:
            logger.error(f"{er}")
        finally:
            await db.commit()


def _register_register_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(__start, commands=["start"], state='*')

