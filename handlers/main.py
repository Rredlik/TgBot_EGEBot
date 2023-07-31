import logging

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from loguru import logger

from config import ADMIN_IDS
from config.env import Env
from filters import register_all_filters
from handlers.admin import register_admin_handlers
from handlers.keyboards import kb_main
from handlers.stuff_methods import _register_utils_handlers
from handlers.user.main import register_users_handlers
# from misc.scheduler_jobs import register_jobs


async def register_all_handlers(dp: Dispatcher) -> None:
    handlers = (
        register_admin_handlers,
        register_users_handlers,
        _register_utils_handlers
    )
    for handler in handlers:
        handler(dp)


async def __on_start_up(dp: Dispatcher):
    # await register_database()
    await register_all_filters(dp)
    await register_all_handlers(dp)
    # await register_jobs(dp)

    logger.success("Bot started!")
    logger.info(f"Admins list: {ADMIN_IDS}")
    # for user in ADMIN_IDS:
    await dp.bot.send_message(chat_id=351931465, text='Бот перезапущен!', reply_markup=await kb_main())


async def __on_shutdown(dp):
    logger.info("Bot stopped!\n")


def start_telegram_bot():
    # logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    #                     level=logging.DEBUG)
    # logger = logging.getLogger(__name__)
    # bot = Bot(token=Env.TOKEN, parse_mode='HTML')
    TOKEN = '5526113848:AAHXJKLH5BEDyogSFUbaupnrE1H2NoehBoI'
    bot = Bot(token=TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())
    executor.start_polling(dp,  skip_updates=True, on_startup=__on_start_up, on_shutdown=__on_shutdown)
