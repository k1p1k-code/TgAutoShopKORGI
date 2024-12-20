from routers import admin_router
from loader import dp, bot, cfg
from aiogram import types, F
from keyb import admin 
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import json
from data import json_utils

class edit_tests(StatesGroup):
    hello=State()
    profile=State()
    helpp=State()

@admin_router.callback_query(F.data == 'settings_open')
async def switch_menu(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    PATH='data/settings.json'
    data=json.load((open(PATH, 'r', encoding='UTF-8')))

    iswork='Работает' if data['work'] == True else 'Не работает'
    await call.message.edit_text(f'<b>🤖 Статус: {iswork}</b>', reply_markup=await admin.get_settings_menu(), parse_mode="HTML")

@admin_router.callback_query(F.data == 'onoff_bot_work_admin')
async def onoff_bot(call: types.CallbackQuery):
    PATH='data/settings.json'
    data=json.load((open(PATH, 'r', encoding='UTF-8')))
    if data['work'] == True:
        data['work']=False
    else:
        data['work']=True
    json.dump(fp=open(PATH, 'w', encoding='UTF-8'), obj=data, indent=4)
    data=json.load((open(PATH, 'r', encoding='UTF-8')))
    iswork='Работает' if data['work'] == True else 'Не работает'
    await call.message.edit_text(f'<b>🤖 Статус: {iswork}</b>', reply_markup=await admin.get_settings_menu(), parse_mode="HTML")

@admin_router.callback_query(F.data == 'bot_text_menu_admin')
async def text_menu_admin(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(text='<b>✍️ Здесь ты можешь изменить текст для пользователей</b>', reply_markup=await admin.get_texts_menu(), parse_mode="HTML")


@admin_router.callback_query(F.data == 'edit_text_hello_admin')
async def edit_text_hello_admin(call: types.CallbackQuery, state: FSMContext):
    back_main=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='🔙', callback_data='bot_text_menu_admin')]])
    await state.set_state(edit_tests.hello)
    msg=await call.message.edit_text(text='<b>✍️ Введите новое приведствие\n🔗 Подержка: HTML\n<code>{username}</code> - юзернайм\n<code>{full_name}</code> - полное имя\n<code>{fist_name}</code> - имя\n<code>{id}</code> - id</b>', reply_markup=back_main, parse_mode="HTML")
    await state.update_data(msg_id=msg.message_id)

@admin_router.message(edit_tests.hello)
async def edit_hello(message: types.Message, state: FSMContext):
    await message.delete()
    await json_utils.edit_text(text='start', value=message.text)
    data=await state.update_data()
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['msg_id'], text='<b>✅Готово\n✍️ Здесь ты можешь изменить текст для пользователей</b>', reply_markup=await admin.get_texts_menu(), parse_mode="HTML")
    await state.clear()

@admin_router.callback_query(F.data == 'edit_text_profile_admin')
async def edit_text_profile_admin(call: types.CallbackQuery, state: FSMContext):
    back_main=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='🔙', callback_data='bot_text_menu_admin')]])
    await state.set_state(edit_tests.profile)
    msg=await call.message.edit_text(text='<b>✍️ Введите новый текст для профиля\n🔗 Подержка: HTML\n<code>{username}</code> - юзернайм\n<code>{full_name}</code> - полное имя\n<code>{fist_name}</code> - имя\n<code>{id}</code> - id\n<code>{balance}</code> - баланс\n<code>{time}</code> - время регистрации</b>', reply_markup=back_main, parse_mode="HTML")
    await state.update_data(msg_id=msg.message_id)

@admin_router.message(edit_tests.profile)
async def edit_hello(message: types.Message, state: FSMContext):
    await message.delete()
    await json_utils.edit_text(text='profile', value=message.text)
    data=await state.update_data()
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['msg_id'], text='<b>✅Готово\n✍️ Здесь ты можешь изменить текст для пользователей</b>', reply_markup=await admin.get_texts_menu(), parse_mode="HTML")
    await state.clear()

@admin_router.callback_query(F.data == 'edit_text_help_admin')
async def edit_text_hello_admin(call: types.CallbackQuery, state: FSMContext):
    back_main=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='🔙', callback_data='bot_text_menu_admin')]])
    await state.set_state(edit_tests.helpp)
    msg=await call.message.edit_text(text='<b>✍️ Введите новый текст для помощи\n🔗 Подержка: HTML\n<code>{username}</code> - юзернайм\n<code>{full_name}</code> - полное имя\n<code>{fist_name}</code> - имя\n<code>{id}</code> - id\n<code>{creator}</code> - ссылка на админа если есть юз</b>', reply_markup=back_main, parse_mode="HTML")
    await state.update_data(msg_id=msg.message_id)

@admin_router.message(edit_tests.helpp)
async def edit_hello(message: types.Message, state: FSMContext):
    await message.delete()
    await json_utils.edit_text(text='help', value=message.text)
    data=await state.update_data()
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['msg_id'], text='<b>✅Готово\n✍️ Здесь ты можешь изменить текст для пользователей</b>', reply_markup=await admin.get_texts_menu(), parse_mode="HTML")
    await state.clear()