from datetime import datetime

from aiogram import Dispatcher
from aiogram.types import Message
from loguru import logger

from config import connectToDB, CHANNEL_LINK
from handlers.msg_text import MAIN_MENU_TEXT
from handlers.keyboards import *
from handlers.user.user_help import _register_help_handlers


async def __start(message: Message):
    # test_userId = await get_user_by_telegram_id(message.from_user.id)
    # print(f'test_userId: {test_userId}')
    user_id = message.from_user.id
    # first_name = message.from_user.first_name
    # print(user_id)
    value = await is_reg(user_id=user_id)
    # print(f'value: {value}')
    msg_txt = await MAIN_MENU_TEXT()

    if value == 'Register':
        await message.answer("Приветствую! Я - бот канала Саши Зиятдинова.\n\n"
                             "Мы предоставляем бесплатный доступ к урокам по "
                             "программированию на Python за подписку на канал!\n\n"
                             f"Подпишись на наш канал {CHANNEL_LINK} и нажимай на кнопку «Подписка есть»",
                             reply_markup=await check_sub())

    await message.answer(text=msg_txt,
                         reply_markup=await kb_main())


async def is_reg(user_id):
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
                return 'Register'
            else:
                return values
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

