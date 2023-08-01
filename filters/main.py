from aiogram import Dispatcher, Bot
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import Message, ChatMemberStatus, InlineKeyboardMarkup, InlineKeyboardButton

from config import *
from database.methods import user_stage


class IsSubscriber(BoundFilter):
    async def check(self, message: Message):
        bot: Bot = message.bot
        subscribed = 0
        for chat_id in CHANNEL_ID:
            sub_status = await bot.get_chat_member(chat_id=chat_id, user_id=message.from_user.id)

            if sub_status.status != ChatMemberStatus.LEFT:
                subscribed += 1

        if subscribed == len(CHANNEL_ID):
            return True
        else:
            userStage = await user_stage.get(message.from_user.id)
            if userStage == 1:
                stageWord = 'начать'
            else:
                stageWord = 'продолжить'

            markup = InlineKeyboardMarkup() \
                .add(InlineKeyboardButton('✅ Проверить подписку', callback_data='check_sub_second')) \
                .add(InlineKeyboardButton('👩🏼‍💻 Тех. поддержка', url='t.me/skidikis'))
            await bot.send_message(message.from_user.id,
                                   'К сожалению, не вижу твоей подписки. Давай попробуем ещё раз.\n\n'
                                   f'📚Чтобы {stageWord} обучение, подпишись на наш канал {CHANNEL_LINK}\n\n'
                                   'P.s. Если у тебя возникла проблема с подпиской - напиши в тех. поддержку',
                                   reply_markup=markup)
            raise CancelHandler()


class IsAdmin(BoundFilter):
    async def check(self, message: Message):
        return True if message.from_user.id in ADMIN_IDS else False


class NotAdmin(BoundFilter):
    async def check(self, message: Message) -> bool:
        return False if message.from_user.id in ADMIN_IDS else True


async def register_all_filters(dp: Dispatcher):
    filters = (
        NotAdmin,
        IsAdmin,
        IsSubscriber
    )
    for filter in filters:
        dp.bind_filter(filter)
