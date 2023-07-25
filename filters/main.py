from aiogram import Dispatcher, Bot
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import Message, ChatMemberStatus, InlineKeyboardMarkup, InlineKeyboardButton

from config import *


class IsSubscriber(BoundFilter):
    async def check(self, message: Message):
        bot: Bot = message.bot
        for chat_id in CHANNEL_ID:
            sub_status = await bot.get_chat_member(chat_id=chat_id, user_id=message.from_user.id)
            if sub_status.status == ChatMemberStatus.LEFT:
                return False
            else:
                return True


class IsAdmin(BoundFilter):
    async def check(self, message: Message):
        return True if message.from_user.id in ADMIN_IDS else False


class NotAdmin(BoundFilter):
    async def check(self, message: Message) -> bool:
        return False if message.from_user.id in ADMIN_IDS else True


async def register_all_filters(dp: Dispatcher):
    filters = (
        NotAdmin,
        IsAdmin
    )
    for filter in filters:
        dp.bind_filter(filter)
