from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from handlers.msg_text import BTN_CLOSE


async def check_sub():
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton('✅ Проверить подписку',
                                                             callback_data='check_sub'))
    return markup


async def check_sub_second():
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton('✅ Проверить подписку',
                                                             callback_data='check_sub_second'))\
        .add(InlineKeyboardButton('✅ Тех. поддержка', callback_data='@skidikis'))
    return markup


async def to_instruction():
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Далее',
                                                             callback_data='instruction'))
    return markup


async def sub_succeed_cont():
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Да!',
                                                             callback_data='sub_succeed_cont'))
    return markup


async def kb_main():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
        .row(KeyboardButton('✅ Модуль')) \
        .row(KeyboardButton('📚 Тех. поддержка'))

    return markup
