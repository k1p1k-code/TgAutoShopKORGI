from routers import admin_router
from loader import dp, bot
from aiogram import types, F
from keyb import admin 
import asyncio
from aiogram.fsm.context import FSMContext
from data import db
from aiogram.fsm.state import State, StatesGroup
from utils.payment import check_token

class pay_edit(StatesGroup):
    edit_token=State()

@admin_router.callback_query(F.data[:15] == 'colse_edit_pay_')
async def colse_edit_pay(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    pay=call.data[15:]
    pay_data=await db.get_pay(pay=pay)
    token=pay_data[0][2]
    if pay_data[0][2] == '0':
        token='Нету'
    await call.message.edit_text(f'<b>💳 Платежка: {pay}\n🔒 Токен: {token}</b>', reply_markup=await admin.settings_pay(pay=pay), parse_mode='HTML')

@admin_router.callback_query(F.data == 'pay_menu_open')
async def back_mine_admin(call: types.CallbackQuery):

    await call.message.edit_text('<b>💳 Способы оплаты 💳</b>', reply_markup=await admin.admin_paysys_menu(), parse_mode="HTML")

@admin_router.callback_query(F.data[:15] == 'pay_open_admin_')
async def pay_open_item_admin(call: types.CallbackQuery):
    pay=call.data[15:]
    pay_data=await db.get_pay(pay=pay)
    token=pay_data[0][2]
    if pay_data[0][2] == '0':
        token='Нету'
    await call.message.edit_text(f'<b>💳 Платежка: {pay}\n🔒 Токен: {token}</b>', reply_markup=await admin.settings_pay(pay=pay), parse_mode='HTML')

@admin_router.callback_query(F.data[:21] == 'pay_edit_token_admin_')
async def pay_edit_token_admin(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(pay_edit.edit_token)
    pay=call.data[21:]
    msg=await call.message.edit_text(f'<b>🔐 Отправь токен {pay}</b>', reply_markup=await admin.close_pay(pay=pay), parse_mode='HTML')
    await state.update_data(pay=pay, msg_id=msg.message_id)

@admin_router.message(pay_edit.edit_token)
async def pay_get_token_admin(message: types.Message, state: FSMContext):
    data=await state.get_data()
    await db.replace_pay(item='pay_token', edit=message.text, pay=data['pay'])
    await db.replace_pay(item='pay_onoff', edit=0, pay=data['pay'])
    pay_data=await db.get_pay(pay=data['pay'])
    token=pay_data[0][2]
    if pay_data[0][2] == '0':
        token='Нету'
    await message.delete()
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['msg_id'], text=f'<b>💳 Платежка: {data['pay']}\n🔒 Токен: {token}</b>', reply_markup=await admin.settings_pay(pay=data['pay']), parse_mode='HTML')
    await state.clear()

@admin_router.callback_query(F.data[:21] == 'pay_edit_onoff_admin_')
async def pay_edit_onoff_admin(call: types.CallbackQuery):
    pay=call.data[21:]
    pay_data=await db.get_pay(pay=pay)
    if pay_data[0][1] == 1:
        await db.replace_pay(item='pay_onoff', edit=0, pay=pay)
    elif pay_data[0][1] == 0:
        valid=False
        if pay=='yoomoney' and await check_token.check_yoomoney(pay_data[0][2]):
            valid=True
        elif pay=='cryptobot' and await check_token.check_cryptobot(pay_data[0][2]):
            valid=True
        elif pay=='lolz' and await check_token.check_lolz(pay_data[0][2]):
            valid=True
        if valid:
            await db.replace_pay(item='pay_onoff', edit=1, pay=pay)
        else:
            return call.answer('❌ Токен недействительный ❌', show_alert=True)
    token=pay_data[0][2]
    if pay_data[0][2] == '0':
        token='Нету'
    await call.message.edit_text(text=f'<b>💳 Платежка: {pay}\n🔒 Токен: {token}</b>', reply_markup=await admin.settings_pay(pay=pay), parse_mode='HTML')