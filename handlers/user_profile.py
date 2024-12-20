from loader import dp, bot, cfg
from aiogram import types, F
from keyb import user 
from data import db
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
from utils import payment, check_spam
from utils.payment import check_payment
import os
from random import randint
from datetime import datetime
import time as timee
from data.json_utils import get_texts
import json

class Profile(StatesGroup):
    pay_sum=State()

async def get_text_profile(time, balance, call):
    return (await get_texts())['profile'].format(username=call.from_user.username,
                                                full_name=call.from_user.full_name,
                                                fist_name=call.from_user.first_name,
                                                id=call.from_user.id, 
                                                balance=balance,
                                                time=time,
                                                call=call)

@dp.callback_query(F.data.startswith('open_profile'))
async def open_profile(call: types.CallbackQuery):
    data_user=await db.get_dataUser(user_id=call.from_user.id)
    time=datetime.utcfromtimestamp(data_user[0][2]).strftime('%Y-%m-%d %H:%M:%S')
    await call.message.edit_text(await get_text_profile(time=time, balance=data_user[0][1], call=call), reply_markup=await user.user_profile_menu(), parse_mode="HTML")

@dp.callback_query(F.data == 'back_profile')
async def back_profile(call: types.CallbackQuery, state: FSMContext):
    data_user=await db.get_dataUser(user_id=call.from_user.id)
    time=datetime.utcfromtimestamp(data_user[0][2]).strftime('%Y-%m-%d %H:%M:%S')
    await call.message.edit_text(await get_text_profile(time=time, balance=data_user[0][1], call=call), reply_markup=await user.user_profile_menu(), parse_mode="HTML")
    await state.clear()

@dp.callback_query(F.data == 'start_pay')
async def start_pay(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Profile.pay_sum)
    msg=await call.message.edit_text('<b>💵 Веди сумму на которую хочешь пополнить </b>',reply_markup=types.InlineKeyboardMarkup(inline_keyboard=user.back_profile), parse_mode="HTML")
    await state.update_data(msg_id=msg.message_id)

@dp.message(Profile.pay_sum)
async def  get_sum_pay(message: types.Message, state: FSMContext):
    await message.delete()
    data=await state.get_data()
    try:
        summ=int(message.text)
    except:
        return
    if type(summ) != type(int()):
        return
    await bot.edit_message_text(message_id=data['msg_id'], chat_id=message.from_user.id, text=f'<b>💳 Выбери платежную систему\n💵 К оплате: {summ}₽</b>', reply_markup=await user.user_ch_syspay(summ=message.text), parse_mode="HTML")
    await state.clear()

@dp.callback_query(F.data[:12] == 'pay_profile_')
async def pay_profile(call: types.CallbackQuery):
    pay, summ = call.data.split('_')[2], call.data.split('_')[3]
    pay_data=await db.get_pay(pay=pay)
    
    comment=f'{call.from_user.id}:{randint(100, 999)}'
    if pay == 'lolz':
        payments=await payment.create_lolz(summ=summ, token=pay_data[0][2], comment=comment)
        link=payments['link']
        await call.message.edit_text(text=f'<b>💵 К оплате: {summ}₽\nВажно⚠️\n❗️Сумма даже быть: {summ}₽\n❗️ Коментарий не должен менятся\n❗️ Не ставьте не каких галочек</b>', reply_markup=await user.pay_check(link=link, pay=pay, comment=comment, summ=summ), parse_mode="HTML")

    elif pay == 'yoomoney': 
        payments=await payment.create_yoomoney(summ=summ, token=pay_data[0][2], comment=comment)
        link=payments['link']
        await call.message.edit_text(text=f'<b>💵 К оплате: {summ}₽</b>', reply_markup=await user.pay_check(link=link, pay=pay, comment=comment, summ=summ), parse_mode="HTML")

@dp.callback_query(F.data[:18] == 'pay_check_profile_')
async def pay_check_profile(call: types.CallbackQuery):
    if await check_spam(user_id=call.from_user.id):
        return await call.answer('🕓 Подождите')

    pay, comment, summ = call.data.split('_')[4], call.data.split('_')[3], call.data.split('_')[5]
    data=await db.get_pay(pay=pay)
    if pay == 'lolz':
        if await check_payment.check_lolz(token=data[0][2], summ=summ, comment=comment) or call.from_user.id == cfg.admin_id:
            await db.get_balance(summ=summ, user_id=call.from_user.id)
            data_user=await db.get_dataUser(user_id=call.from_user.id)
            time=datetime.utcfromtimestamp(data_user[0][2]).strftime('%Y-%m-%d %H:%M:%S')
            await call.message.edit_text(f'<b>✅ +{summ}₽</b>\n' + await get_text_profile(time, data_user[0][1], call), reply_markup=await user.user_profile_menu(), parse_mode="HTML")
            u=f"<a href='tg://user?id={call.from_user.id}'>{call.from_user.first_name}</a>" 
            PATH='data/settings.json'
            data_json=json.load((open(PATH, 'r', encoding='UTF-8')))
            if data_json['nofication']['puy']:
                await bot.send_message(chat_id=cfg.admin_id, text=f'<b>Пополнение\nСумма: {summ}\n Пользователь: </b>{u}', parse_mode='HTML') 
            
        else:
            return await call.answer('⛔️ Оплата не найдена ⛔️', show_alert=True)
    
    elif pay == 'yoomoney':
        if await check_payment.check_yoomoney(token=data[0][2], summ=summ, comment=comment) or call.from_user.id == cfg.admin_id:
            print(data[0][2])
            await db.get_balance(summ=summ, user_id=call.from_user.id)
            data_user=await db.get_dataUser(user_id=call.from_user.id)
            time=datetime.utcfromtimestamp(data_user[0][2]).strftime('%Y-%m-%d %H:%M:%S')
            await call.message.edit_text(f'<b>✅ +{summ}₽</b>\n' + await get_text_profile(time, data_user[0][1], call), reply_markup=await user.user_profile_menu(), parse_mode="HTML")
            u=f"<a href='tg://user?id={call.from_user.id}'>{call.from_user.first_name}</a>" 
            PATH='data/settings.json'
            data_json=json.load((open(PATH, 'r', encoding='UTF-8')))
            if data_json['nofication']['buy']:
                await bot.send_message(chat_id=cfg.admin_id, text=f'<b>➕ Пополнение\n💵 Сумма: {summ}₽\n👨 Пользователь: </b>{u}', parse_mode='HTML') 
        else:
            return await call.answer('⛔️ Оплата не найдена ⛔️', show_alert=True)
    

@dp.callback_query(F.data == 'my_buyer')
async def my_buyer(call: types.CallbackQuery):
    history=await db.get_history(id=call.from_user.id, item='history_user')
    if history == list():
        return await call.answer('❌ Нет покупок')
    text_loger=str()
    for i in history:
        if i[0] == 'product':
            time=datetime.utcfromtimestamp(i[6]).strftime('%Y-%m-%d %H:%M:%S')
            text_loger+=f'<p><p><b>{i[2]}</p>\n<p>🗳Тип: товар</p>\n<p>🆔 {i[1]}</p>\n<p>🔢Сумма: {i[4]}₽</p>\n<p>👤 Купил: <a href="tg://user?id={i[5]}">{i[5]}</a></p>\n<p>🕘 В: {time}</p>\n<p>🗞 Выданные данные: {i[3]}</b><p>\n\n------------------\n\n</p></p></p>'

    PATH=f'data//temp_bot//history_{timee.time()}_{call.from_user.id}.html'
    file=open(PATH, 'w', encoding='UTF-8')
    file.write(text_loger)
    file.close()
    document = FSInputFile(PATH)
    await call.message.answer_document(document, caption='❗️ Возможно с chrome(mobile) не работает')
    os.remove(PATH)
