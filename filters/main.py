from aiogram import Dispatcher, Bot
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import Message, ChatMemberStatus, InlineKeyboardMarkup, InlineKeyboardButton

from config import *


class IsSubscriber(BoundFilter):
    async def check(self, message: Message):
        bot: Bot = message.bot
        subscribed = 0
        print(f'cheking sub')
        # try:
        print('##try')
        for chat_id in CHANNEL_ID:
            sub_status = await bot.get_chat_member(chat_id=chat_id, user_id=message.from_user.id)
            print(f'sub_status: {sub_status}')

            if sub_status.status != ChatMemberStatus.LEFT:
                print('sub')
                subscribed += 1
            else:
                print('not sub')
                break
        # else:
        if subscribed == len(CHANNEL_ID):
            print('sub 2')
            return True
        else:
            print('not sub 2')
            markup = InlineKeyboardMarkup().add(InlineKeyboardButton('Подписаться',
                                                                     url='https://t.me/rredlik'))
            await bot.send_message(chat_id=message.from_user.id,
                                      text='Чтобы пользоваться ботом, подпишись на канал:',
                                      reply_markup=markup)
            raise CancelHandler()
        # except Exception as er:
        #     print(f'[[ERROR]{datetime.now()} {inspect.getframeinfo(inspect.currentframe()).function}]: {er}')


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
