import asyncio

from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery, ContentType
from aiogram.utils import exceptions
from loguru import logger

from database.methods.other import parseAllUsers
from filters.main import IsAdmin
from handlers.admin.media import _register_media_handlers
from handlers.keyboards import kb_main
from utils.states import ADPosting


async def __admin_menu(msg: Message, state: FSMContext):
    userId = msg.from_user.id
    message_txt = 'Меню специальных функций администратора\n\n' \
                  '- Информация о боте\n' \
                  '- Рассылка для всех пользователей'
    markup = InlineKeyboardMarkup() \
        .add(InlineKeyboardButton('Информация', callback_data='analytic')) \
        .add(InlineKeyboardButton('Рассылка', callback_data='adPosting'))

    await msg.bot.send_message(userId, message_txt, reply_markup=markup)
    logger.info(f'User_id: {userId}')


# endregion

# region Advertising

async def __write_AdPost(query: CallbackQuery, state: FSMContext):
    await state.reset_state()
    text = '📷 Фото: выбери одну фотографию и напиши текст поста\n' \
                  '🎥 Видео: выбери одно видео и напиши текст поста\n\n' \
                  'Специальные правила оформления для текста:\n' \
                  '&lt;a href="ссылка"&gt;текст с сылкой&lt;/a&gt;\n' \
                  '&lt;b&gt;<b>Полужирный текст</b>&lt;/b&gt;\n' \
                  '&lt;i&gt;<i>Текст курсив</i>&lt;/i&gt;\n\n' \
                  'Введите текст сообщения для рассылки, либо нажмите отмена\n\n'
    markup = InlineKeyboardMarkup() \
        .add(InlineKeyboardButton('Отмена', callback_data='close_menu_'))

    await query.bot.send_message(query.from_user.id, text, reply_markup=markup)
    await ADPosting.WriteText.set()


async def __check_AdPost(msg: Message, state: FSMContext, image=None, video=None):
    bot: Bot = msg.bot
    userId = msg.from_user.id
    await ADPosting.CheckPost.set()
    addText = '\n\n⬆⬆⬆\nПроверьте сообщение и нажмите "Отправить", если все хорошо, иначе нажмите "Исправить"'
    markup = InlineKeyboardMarkup() \
        .add(InlineKeyboardButton('Отправить', callback_data='sendAdPost')) \
        .add(InlineKeyboardButton('Исправить', callback_data='adPosting'))

    if msg.content_type == ContentType.PHOTO:
        image = msg.photo[0].file_id
        msgText = msg.caption if msg.caption else ''
        await bot.send_photo(userId, image, msgText + addText, reply_markup=markup)
    elif msg.content_type == ContentType.VIDEO:
        video = msg.video.file_id
        msgText = msg.caption if msg.caption else ''
        await bot.send_video(userId, video, msgText + addText, reply_markup=markup)
    else:
        msgText = msg.text
        await bot.send_message(userId, msgText + addText, reply_markup=markup)

    async with state.proxy() as data:
        data['msgText'] = msgText
        data['imageId'] = image
        data['videoId'] = video
    await ADPosting.SendPost.set()


async def __send_AdPost(query: CallbackQuery, state: FSMContext):
    bot: Bot = query.bot
    dataS = await state.get_data()
    print(f'dataS: {dataS}')
    async with state.proxy() as data:
        msgText = data['msgText']
        image = data['imageId']
        video = data['videoId']
    await state.reset_state()
    await bot.send_message(query.from_user.id, 'Рассылка начата✅', reply_markup=await kb_main())
    count = await broadcaster(bot, msgText, image, video)
    await bot.send_message(query.from_user.id, f'{count} пользователя получили сообщение', reply_markup=await kb_main())


async def broadcaster(bot, msgText, image, video) -> int:
    """
    Simple broadcaster
    :return: Count of messages
    """
    allUsers = await parseAllUsers()

    count = 0
    try:
        for user_id in allUsers:
            if await send_message(bot, user_id[0], text=msgText, image=image, video=video):
                count += 1
            await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)
    finally:
        logger.success(f'Рассылка отправлена пользователям - {count}')
    return count


async def send_message(bot, user_id: int, text: str, disable_notification: bool = False, image=False,
                       video=False) -> bool:
    """
    Safe messages sender
    """
    try:
        if image:
            await bot.send_photo(chat_id=user_id, photo=image, caption=text, reply_markup=await kb_main(),
                                 disable_notification=disable_notification)
        elif video:
            await bot.send_video(chat_id=user_id, video=video, caption=text, reply_markup=await kb_main(),
                                 disable_notification=disable_notification)
        else:
            await bot.send_message(chat_id=user_id, text=text, reply_markup=await kb_main(),
                                   disable_notification=disable_notification)

    except exceptions.RetryAfter as e:
        logger.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(bot, user_id, text, disable_notification, image, video)  # Recursive call
    except Exception as er:
        logger.error(f"Target [ID:{user_id}]: {er}")
    else:
        return True
    return False


# endregion
######################################################
######################################################
# region Analytics

async def __analytic(query: CallbackQuery, state: FSMContext) -> None:
    users_count = await parseAllUsers()
    text = (
        'Отчет:\n',
        f'Кол-во пользователей: {len(users_count)}'
    )
    await query.answer('\n'.join(text), show_alert=True, cache_time=0)


def register_admin_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(__admin_menu, IsAdmin(), commands=['admin'],
                                state='*')
    # endregion

    # region Advertising
    dp.register_callback_query_handler(__write_AdPost, lambda c: c.data == 'adPosting',
                                       IsAdmin(), state='*')
    dp.register_message_handler(__check_AdPost, IsAdmin(), state=ADPosting.WriteText,
                                content_types=[ContentType.PHOTO, ContentType.VIDEO, ContentType.TEXT])
    dp.register_callback_query_handler(__send_AdPost, lambda c: c.data == 'sendAdPost',
                                       IsAdmin(), state=ADPosting.SendPost)
    # endregion

    # region Analytics
    dp.register_callback_query_handler(__analytic, lambda c: c.data == 'analytic',
                                       IsAdmin(), state='*')
    _register_media_handlers(dp)
    # endregion
