import asyncio
import inspect
from datetime import datetime

from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from loguru import logger

import handlers.main
from config import ADMIN_IDS, connectToDB
from filters.main import IsAdmin
from handlers.keyboards import kb_main


async def send_photo_file_id(msg: Message, state: FSMContext):
    print(await state.get_state())
    bot: Bot = msg.bot
    photo_id = msg.photo[-1].file_id
    rest_name = str(msg.caption).lower()
    markup = await kb_main()

    async with connectToDB() as db:
        try:
            select_rest = await db.execute(
                f"SELECT id, name, image FROM rests where small_name like '%{rest_name}%'"
            )
            rest_info = await select_rest.fetchall()
            # print('rest_info', rest_info)
            rest_id, name, image = rest_info[0]
            # if image is None or '':
            await db.execute(
                f"UPDATE 'rests' SET image = :photo_id WHERE id = :rest_id",
                {'rest_id': rest_id, 'photo_id': photo_id}
            )
            await db.commit()
            await msg.reply(photo_id)
            await bot.send_photo(chat_id=msg.chat.id,
                                 photo=photo_id,
                                 caption=f'Измененно изображение ресторана\n '
                                         f'<b>{name}</b> - id: {rest_id}',
                                 parse_mode='html',
                                 reply_markup=markup)

        except Exception as er:
            msgText = (f'{photo_id}\n\n'
                                  '‼ Произошла ошибка, фото не присвоено к ресторану. ‼\n\n'
                                                    'Проверьте введенное название, возможно его нет в базе или допущена опечатка. '
                                        'В качестве названия принимаются только буквы.\n\n'
                                        '❗ Если в названии есть символы - : _ \ / № # @ и тп., '
                                        'введите текст стоящий до или после них\n'
                                        'Пример: Морская_10 -> Морская\n\n'
                                        '❗ Буквы й, ё могут быть неправильными, лучше '
                                        'ввести часть слова до или после них, '
                                        'либо скопировать символ отправленный по соответсвующей кнопке, '
                                        'если слово слишком короткое (менее 3х букв).\n\n'
                                        'Регистр не имеет значения\n'
                                        'Если не работает, обратится в тех.поддержку и '
                                        'внести данные в базу в ручном режиме')
            logger.error(er)
            markup = InlineKeyboardMarkup() \
                .row(InlineKeyboardButton('Отправить Й', callback_data='letter_й'),
                     InlineKeyboardButton('Отправить Ё', callback_data='letter_ё'))
            await bot.send_message(chat_id=msg.chat.id,
                                   text=msgText,
                                   reply_markup=markup)
        finally:
            await db.commit()


async def __sendLetters(query: CallbackQuery):
    bot: Bot = query.bot
    letter = query.data.split('_')[1]
    await bot.send_message(chat_id=query.from_user.id,
                           text=letter)


async def __send_video_file_id(message: Message):
    msgText = f'Хорошее видео, сохранил 😊'
    video_id = message.video.file_id
    if message.from_user.id in ADMIN_IDS:
        msgText += f'\n\nId видео файла: {video_id}'
    logger.success(f'Video_id: {video_id}')
    await message.reply(text=msgText)


def _register_media_handlers(dp: Dispatcher) -> None:
    # region Media

    dp.register_message_handler(send_photo_file_id, IsAdmin(), content_types=ContentType.PHOTO)

    dp.register_callback_query_handler(__sendLetters, IsAdmin(), lambda c: c.data and c.data.startswith('letter_'))

    dp.register_message_handler(__send_video_file_id, content_types=ContentType.VIDEO)
