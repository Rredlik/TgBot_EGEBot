from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from handlers.msg_text import BTN_CLOSE


async def check_sub():
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton('✅ Проверить подписку',
                                                             callback_data='check_sub'))
    return markup


async def kb_main():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
        .row(KeyboardButton('✅ Подобрать заведение'), KeyboardButton('🔀 Случайное заведение')) \
        .row(KeyboardButton('⭐ Избранные'), KeyboardButton('🏆 ТОП-месяца'), KeyboardButton('📚 Инструкция'))

    return markup


async def openMainKeyboard():
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton('⌨️ Открыть клавиатуру',
                                                             callback_data='close_menu_'))
    return markup


async def kb_close():
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton(BTN_CLOSE, callback_data='close_menu_selected'))
    return markup
