import asyncio

from loguru import logger

from config import set_datetime
from database.main import create_db
from handlers.main import start_telegram_bot
from utils.misc.path import PathManager


def main():

    # log_path = PathManager.get('logs/debug.log')
    # logger.configure(patcher=set_datetime)
    # logger.add(log_path, format="{extra[datetime]} | {level} | {message}",
    #            level="DEBUG", rotation="10:00", compression="zip")
    start_telegram_bot()


if __name__ == '__main__':
    main()
