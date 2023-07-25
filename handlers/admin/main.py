from loguru import logger
from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery, ContentType

from filters.main import IsAdmin
from handlers.admin.database import parseAllUsers
from handlers.admin.media import _register_media_handlers
from handlers.keyboards import kb_main
from handlers.msg_text import BTN_CLOSE
from handlers.stuff_methods import send_mess_or_cb, deletePreviousMessage
from utils.states import ADPosting



async def __admin_menu(msg: Message, state: FSMContext):
    userId = msg.from_user.id
    message_txt = 'Меню специальных функций администратора\n\n' \
                  '- Информация о боте\n' \
                  '- Рассылка для всех пользователей'
    markup = InlineKeyboardMarkup() \
        .add(InlineKeyboardButton('Информация', callback_data='analytic')) \
        .add(InlineKeyboardButton('Рассылка', callback_data='adPosting')) \
        .add(InlineKeyboardButton(BTN_CLOSE, callback_data='close_menu_'))

    await send_mess_or_cb(msg=msg, message_text=message_txt,
                          markup=markup, state=state)
    logger.info(f'User_id: {userId}')


# endregion

# region Advertising

async def __write_AdPost(query: CallbackQuery, state: FSMContext):
    await state.reset_state()
    message_txt = '📷 Фото: выбери одну фотографию и напиши текст поста\n' \
                  '🎥 Видео: выбери одно видео и напиши текст поста\n\n' \
                  'Специальные правила оформления для текста:\n' \
                  '&lt;a href="ссылка"&gt;текст с сылкой&lt;/a&gt;\n' \
                  '&lt;b&gt;<b>Полужирный текст</b>&lt;/b&gt;\n' \
                  '&lt;i&gt;<i>Текст курсив</i>&lt;/i&gt;\n\n' \
                  'Введите текст сообщения для рассылки, либо нажмите отмена\n\n'
    markup = InlineKeyboardMarkup() \
        .add(InlineKeyboardButton('Отмена', callback_data='close_menu_'))

    await send_mess_or_cb(query=query, message_text=message_txt,
                          markup=markup, state=state)
    await ADPosting.WriteText.set()


async def __check_AdPost(msg: Message, state: FSMContext, image=None, video=None):
    await ADPosting.CheckPost.set()
    msgText = ''
    if msg.content_type == ContentType.PHOTO:
        image = msg.photo[0].file_id
        print(f'image: {image}')
        msgText += msg.caption if msg.caption else ''
    elif msg.content_type == ContentType.VIDEO:
        video = msg.video.file_id
        print(f'video: {video}')
        msgText += msg.caption if msg.caption else ''
    else:
        msgText += msg.text

    # print(msg)
    print(f'msgText: {msgText}')
    addText = '\n\nПроверьте сообщение и нажмите "Отправить", если все хорошо, иначе нажмите "Исправить"'
    markup = InlineKeyboardMarkup() \
        .add(InlineKeyboardButton('Отправить', callback_data='sendAdPost')) \
        .add(InlineKeyboardButton('Исправить', callback_data='adPosting'))

    await send_mess_or_cb(msg=msg, message_text=msgText + addText, markup=markup, state=state,
                          image=image, video=video)
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
    await send_mess_or_cb(query=query,
                          message_text='Рассылка начата✅',
                          state=state)

    allUsers = await parseAllUsers()
    coll = 0
    for user in allUsers:
        try:
            if image:
                await bot.send_photo(chat_id=user[0], photo=image, caption=msgText, reply_markup=await kb_main())
            elif video:
                await bot.send_video(chat_id=user[0], video=video, caption=msgText, reply_markup=await kb_main())
            else:
                await bot.send_message(chat_id=user[0], text=msgText, reply_markup=await kb_main())

            coll += 1
        except Exception as er:
            logger.error(er)
            continue
    await send_mess_or_cb(query=query,
                          message_text=f'{coll} пользователя получили сообщение',
                          state=state)
    logger.success(f'Рассылка отправлена пользователям - {coll}')


# endregion

# region Analytics

async def __analytic(query: CallbackQuery, state: FSMContext) -> None:
    users_count = await parseAllUsers()
    text = (
        'Отчет:\n',
        f'Кол-во пользователей: {len(users_count)}'
    )
    await query.answer('\n'.join(text), show_alert=True, cache_time=0)


def register_admin_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(__admin_menu, IsAdmin(), Text(equals="📚 Инструкция"),
                                state='*')
    # endregion

    # region Advertising

    dp.register_callback_query_handler(__write_AdPost, lambda c: c.data == 'adPosting',
                                       IsAdmin(), state='*')
    dp.register_message_handler(__check_AdPost, IsAdmin(), state=ADPosting.WriteText,
                                content_types=[ContentType.PHOTO, ContentType.VIDEO, ContentType.TEXT])
    # dp.reg

    dp.register_callback_query_handler(__send_AdPost, lambda c: c.data == 'sendAdPost',
                                       IsAdmin(), state=ADPosting.SendPost)
    # endregion

    # region Analytics

    dp.register_callback_query_handler(__analytic, lambda c: c.data == 'analytic',
                                       IsAdmin(), state='*')

    _register_media_handlers(dp)
    # endregion
