from datetime import datetime

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from config import connectToDB
# from handlers.keyboards import openMainKeyboard
from handlers.msg_text import MAIN_MENU_TEXT


# async def register_jobs(dp):
#     scheduler = AsyncIOScheduler()
#     scheduler.add_job(checkUserStates, 'interval', hours=2, args=[dp])
#     # scheduler.add_job(statisticTodayUsers, 'cron', hour='10', args=[dp])
#     scheduler.start()


async def checkUserStates(dp: Dispatcher):
    statesCleaned = 0
    allUsers = await takeLastMsgTime()
    for el in allUsers:
        (userId, lastMsgTime) = el
        if lastMsgTime == '0':
            continue
        lastMsgTime = (datetime.now() - datetime.strptime(lastMsgTime, '%Y-%m-%d %H:%M:%S')).total_seconds()
        if lastMsgTime < 86400:
            continue

        state: FSMContext = FSMContext(
            storage=dp.storage,
            chat=userId,
            user=userId
        )
        curData = await state.get_data()
        message_id = curData.get("messageId")

        try:
            await dp.bot.edit_message_text(chat_id=userId, message_id=message_id,
                                           text=f'{await MAIN_MENU_TEXT()}',
                                           reply_markup="await openMainKeyboard()")
        except Exception as er:
            logger.error(f'{er}')
        finally:
            await updateLastMsgTime(userId, to_delete=True)
        await state.reset_data()
        await state.reset_state()
        async with state.proxy() as data:
            data['messageId'] = message_id
        statesCleaned += 1
    logger.success(f"States cleaned: {statesCleaned}")


async def takeLastMsgTime():
    async with connectToDB() as db:
        try:
            select_rest = await db.execute(
                f"SELECT user_id, last_message_time FROM 'users'"
            )
            await db.commit()
            allUsers = await select_rest.fetchall()
            return allUsers
        except Exception as er:
            logger.error(f'{er}')
        finally:
            await db.commit()


async def updateLastMsgTime(userId, to_delete=False):
    async with connectToDB() as db:
        try:
            if to_delete:
                lastTime = 0
            else:
                lastTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            await db.execute(
                """UPDATE users SET last_message_time = :lastTime WHERE user_id = :userId""",
                {'lastTime': lastTime, 'userId': userId}
            )
        except Exception as er:
            logger.error(f'{er}')
        finally:
            await db.commit()
