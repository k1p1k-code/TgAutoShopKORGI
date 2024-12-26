from core.routers import admin_router
from loader import dp, bot, cfg
from aiogram import types, F
from keyb import admin 
from aiogram.fsm.context import FSMContext
from data import db
from aiogram.fsm.state import State, StatesGroup
from aiogram.types.input_file import FSInputFile
import asyncio
import os
from datetime import datetime
import time as timee

class search_state(StatesGroup):
    user=State()
    payment=State()
    replace_money=State()

@admin_router.callback_query(F.data == 'search_menu_open')
async def open_search(call: types.CallbackQuery):
    await call.message.edit_text(text='<b>Что требуется найти❓</b>', reply_markup=await admin.admin_search(), parse_mode="HTML")

@admin_router.callback_query(F.data == 'search_user')
async def search_payments(call: types.CallbackQuery, state: FSMContext):
    back_main=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='🔙', callback_data='search_menu_open')]])
    await state.set_state(search_state.user)
    msg=await call.message.edit_text(text='<b>🆔 Отправь мне ID пользователя</b>', reply_markup=back_main, parse_mode="HTML")
    await state.update_data(msg_id=msg.message_id)

@admin_router.callback_query(F.data == 'search_payments')
async def search_payments(call: types.CallbackQuery, state: FSMContext):
    back_main=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='🔙', callback_data='search_menu_open')]])
    await state.set_state(search_state.payment)
    msg=await call.message.edit_text(text='<b>🆔 Отправь мне ID заказа</b>', reply_markup=back_main, parse_mode="HTML")
    await state.update_data(msg_id=msg.message_id)

@admin_router.message(search_state.user)
async def get_user(message: types.Message, state: FSMContext):
    await message.delete()
    data=await state.update_data()
    user=await db.get_dataUser(message.text)
    back_main=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='🔙', callback_data='search_menu_open')]])
    if user == list():
        try:
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['msg_id'], text='<b>❌ ID не найден\n🆔 Отправь мне ID пользователя</b>', reply_markup=back_main, parse_mode="HTML")
        except:
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['msg_id'], text='<b>⚠️ ID не найден\n🆔 Отправь мне ID пользователя</b>', reply_markup=back_main, parse_mode="HTML")
        return
    time=datetime.utcfromtimestamp(user[0][2]).strftime('%Y-%m-%d %H:%M:%S')
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['msg_id'], text=f'<b>💰 Баланс: {user[0][1]}₽\n🆔: <a href="tg://user?id={user[0][0]}">{user[0][0]}</a>\n🕧 Дата регистрации: {time}</b>', reply_markup=await admin.get_settings_user(user[0][0]), parse_mode="HTML")

@admin_router.message(search_state.payment)
async def get_payment(message: types.Message, state: FSMContext):
    await message.delete()
    data=await state.update_data()
    history=await db.get_history(message.text)
    back_main=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='🔙', callback_data='search_menu_open')]])
    if history == list():
        try:
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['msg_id'], text='<b>❌ ID не найден\n🆔 Отправь мне ID заказа</b>', reply_markup=back_main, parse_mode="HTML")
        except:
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['msg_id'], text='<b>⚠️ ID не найден\n🆔 Отправь мне ID заказа</b>', reply_markup=back_main, parse_mode="HTML")
        return
    typee=history[0][0].replace('product', 'Товар')
    product=f'📦 Товар: {history[0][2] if history[0][2] != '0' else ''}\n'
    time=time=datetime.utcfromtimestamp(history[0][6]).strftime('%Y-%m-%d %H:%M:%S')
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['msg_id'], text=f'<b>{product}🗳Тип: {typee}\n🆔 {history[0][1]}\n🔢Сумма: {history[0][4]}₽\n👤 Купил: <a href="tg://user?id={history[0][5]}">{history[0][5]}</a>\n🕘 В: {time}\n🗞 Выданные данные: {history[0][3]}</b>', reply_markup=back_main, parse_mode="HTML")



@admin_router.callback_query(F.data[:22] == 'user_edit_money_admin_')
async def user_edit_money_admin(call: types.CallbackQuery, state: FSMContext):
    user_id=call.data[22:]
    back_main=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='📣 Уведомлять: 🟢', callback_data='nofication_replacemoney_onoff')], [types.InlineKeyboardButton(text='🔙', callback_data='search_menu_open')]])
    await state.set_state(search_state.replace_money)
    msg=await call.message.edit_text(text=f'<b>💵 Отправь новое количество денег</b>', reply_markup=back_main, parse_mode="HTML")
    await state.update_data(user_id=user_id, msg_id=msg.message_id, nofication=True)

@admin_router.message(search_state.replace_money)
async def replace_money(message: types.Message, state: FSMContext):
    await message.delete()
    try:
        money=int(message.text)
    except:
        return
    data=await state.update_data()
    await db.replace_balance(summ=money, user_id=data['user_id'])
    user=await db.get_dataUser(user_id=data['user_id'])
    time=datetime.utcfromtimestamp(user[0][2]).strftime('%Y-%m-%d %H:%M:%S')
    if data['nofication']:
        await bot.send_message(chat_id=data['user_id'], text=f'<b>⚙️ Ваш баланс изменил админ\n💰 Баланс: {user[0][1]}</b>', parse_mode="HTML")
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['msg_id'], text=f'<b>💰 Баланс: {user[0][1]}₽\n🆔: <a href="tg://user?id={user[0][0]}">{user[0][0]}</a>\n🕧 Дата регистрации: {time}</b>', reply_markup=await admin.get_settings_user(user[0][0]), parse_mode="HTML")

@admin_router.callback_query(F.data == 'nofication_replacemoney_onoff', search_state.replace_money)
async def onoff_nofication_replacemoney(call: types.CallbackQuery, state: FSMContext):
    data=await state.update_data()
    if data['nofication']:
        await state.update_data(nofication=False)
        signal='🔴'
    else:
        await state.update_data(nofication=True)
        signal='🟢'
    back_main=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text=f'📣 Уведомлять: {signal}', callback_data='nofication_replacemoney_onoff')], [types.InlineKeyboardButton(text='🔙', callback_data='search_menu_open')]])
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=data['msg_id'], reply_markup=back_main)


@admin_router.callback_query(F.data[:20] == 'user_edit_ban_admin_')
async def user_baned(call: types.CallbackQuery):
    user_id=call.data[20:]
    user=await db.get_dataUser(user_id)
    if user[0][3]:
        await db.replace_user(item='user_status', edit=False, user_id=user_id)
    else:
        await db.replace_user(item='user_status', edit=True, user_id=user_id)
    await call.message.edit_reply_markup(reply_markup=await admin.get_settings_user(user_id))

@admin_router.callback_query(F.data[:24] == 'user_show_history_admin_')
async def user_show_history_admin(call: types.CallbackQuery):
    user_id=call.data[24:]
    history=await db.get_history(id=user_id, item='history_user')
    if history == list():
        return await call.answer('❌ Нет записей')
    text_loger=str()
    for i in history:
        if i[0] == 'product':
            time=datetime.utcfromtimestamp(i[6]).strftime('%Y-%m-%d %H:%M:%S')
            text_loger+=f'<p><p><b>{i[2]}</p>\n<p>🗳Тип: товар</p>\n<p>🆔 {i[1]}</p>\n<p>🔢Сумма: {i[4]}₽</p>\n<p>👤 Купил: <a href="tg://user?id={i[5]}">{i[5]}</a></p>\n<p>🕘 В: {time}</p>\n<p>🗞 Выданные данные: {i[3]}</b><p>\n\n------------------\n\n</p></p></p>'

    PATH=f'data\\temp_bot\\history_{timee.time()}_{user_id}.html'
    file=open(PATH, 'w', encoding='UTF-8')
    file.write(text_loger)
    file.close()
    document = FSInputFile(PATH)
    await call.message.answer_document(document)
    os.remove(PATH)
