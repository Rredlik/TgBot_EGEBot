import asyncio

from aiogram import Dispatcher
from aiogram.types import Message

from database.methods.lesson_module import get_one
from filters.main import IsSubscriber
from handlers.keyboards import kb_main


async def __openModule(msg: Message):
    name = msg.text
    module_id, name, description, link = await get_one(name)
    # markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Ссылка на курс', url=link))
    await msg.bot.send_message(chat_id=msg.from_user.id,
                               text=f'{description}\n\n',
                               reply_markup=await kb_main())
    await asyncio.sleep(0.2)
    await msg.bot.send_message(chat_id=msg.from_user.id,
                               text=f'{link}',
                               reply_markup=await kb_main())


def register_openModule_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(__openModule, lambda msg: msg.text.startswith('Модуль'), IsSubscriber())
