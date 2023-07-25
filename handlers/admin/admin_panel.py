### NOT WORKING ###
from aiogram import Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

import handlers.main
from DB_update import update_full_description, get_full_description
from utils.states import RestStates
from handlers.msg_text import MAIN_MENU_TEXT
from handlers.admin.database import create_new_rest, delete_new_rest, add_type_new_rest
from handlers.keyboards import kb_main


#################################### STEP 1


# first btn
async def stage_name(query: CallbackQuery):
    bot: Bot = query.bot
    print("Stage 1 start")
    await RestStates.STATE_1_NAME.set()

    user_id = query.from_user.id
    await bot.send_message(chat_id=user_id,
                           text="Введи название нового заведения без лишних символов и переносов",
                           reply_markup=await new_rest_state_0())
    print('Stage 1 complete')


async def new_rest_state_0():
    markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton('❌ Отмена', callback_data='admin_help_menu_cancel_create_0'))
    return markup


#################################### STEP 2
async def stage_type(message: Message, state: FSMContext):
    print("Stage 2")
    user_id = message.from_user.id
    rest_name = message.text
    rest_id = await create_new_rest(rest_name)
    await update_full_description(False, rest_id)

    name, full_description, image = await get_full_description(rest_id)

    async with state.proxy() as data:
        data['name'] = rest_id

    await RestStates.next()

    await bot.send_message(chat_id=user_id,
                                              text=f"Предпросмотр карточки заведения (id: {rest_id}):\n"
                                   f"{full_description}\n\n"
                                   "Далее, введите тип нового заведения",
                                              parse_mode='html',
                                              reply_markup=await new_rest_state_kb(rest_id))

    print("Stage 2 complete")




# def register_handlers_help(dp: Dispatcher):
#
#     dp.register_message_handler(admin_help_menu, Text(equals="📚 Инструкция"), user_id=ADMIN_IDS)
#
#     dp.register_callback_query_handler(cancel_new_rest,
#                                        lambda c: c.data and c.data.startswith('admin_panel_cancel_'))
#
#     dp.register_message_handler(stage_type,
#                                 state=RestStates.STATE_1_NAME)
#     dp.register_message_handler(stage_kitchen,
#                                 state=RestStates.STATE_2_TYPE)
#     dp.register_message_handler(stage_kitchen,
#                                 state=RestStates.STATE_3_KITCHEN)
#     dp.register_message_handler(stage_type,
#                                 state=RestStates.STATE_4_DESCRIPT)
#     dp.register_message_handler(stage_kitchen,
#                                 state=RestStates.STATE_5_CHECK)
#     dp.register_message_handler(stage_type,
#                                 state=RestStates.STATE_6_ADDRESS)
#     dp.register_message_handler(stage_type,
#                                 state=RestStates.STATE_7_MENU)
#     dp.register_message_handler(stage_kitchen,
#                                 state=RestStates.STATE_8_VIEW)
#     dp.register_message_handler(stage_type,
#                                 state=RestStates.STATE_9_IMAGE)
#
#     dp.register_callback_query_handler(admin_help_menu_cancel_create_0,
#                                        lambda c: c.data == 'admin_help_menu_cancel_create_0',
#                                        state='*',
#                                        user_id=ADMIN_IDS)
#
#     dp.register_callback_query_handler(stage_name,
#                                        lambda c: c.data == 'btn_create_new_rest',
#                                        state='*',
#                                        user_id=ADMIN_IDS)
#
#     dp.register_callback_query_handler(admin_help_function, lambda c: c.data == 'btn_admin_help')
#     dp.register_callback_query_handler(btn_back_main_menu, lambda c: c.data == 'admin_panel_back_to_main')
