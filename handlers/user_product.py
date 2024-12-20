from loader import dp, bot, cfg
from aiogram import types, F
from keyb import user 
from data import db
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from utils import check_spam
import json



class product_user_state(StatesGroup):
    lens_product=State()

async def nofication_pay(ID, product, balance, lens, price, id_history):
    await bot.send_message(chat_id=cfg.admin_id, text=f'<b>🛒 Пользователь купил товар\n💎 Товар: {product}\n💎 Цена покупки: {price}\n🔢 Количество: {lens}\n🆔 <a href="tg://user?id={ID}">{ID}</a>\n💰 Остаток на балансе: {balance}\nID покупки: {id_history}</b>', parse_mode="HTML")

@dp.callback_query(F.data == 'open_main_product_0')
async def open_product(call: types.CallbackQuery):
    await call.message.edit_text('Выбирай что надо', reply_markup=await user.get_catalog(req='0'))

@dp.callback_query(F.data[:18] == 'open_catalog_user_')
async def open_catalog_user(call: types.CallbackQuery):
    req=call.data[18:]
    ctg=await db.get_catalog(ctg_id=req)
    if ctg[0][3] == '0':
        return await call.message.edit_text(f'{ctg[0][2]}', reply_markup=await user.get_catalog(req=req), parse_mode="HTML")
    await call.message.delete()
    await call.answer_photo(photo=cfg[0][3], caption=f'{ctg[0][2]}', reply_markup=await user.get_catalog(req=req), parse_mode="HTML")

@dp.callback_query(F.data[:18] == 'open_product_user_')
async def open_catalog_user(call: types.CallbackQuery):
    req=call.data[18:]
    prd=await db.get_product(prd_id=req)
    logs_len=len(await db.get_log(prd_id=prd[0][0])) if not prd[0][5] else '∞'
    if prd[0][3] == '0':
        return await call.message.edit_text(f'<b>🏷 {prd[0][1]}</b>\n\n<b>💎 ЦЕНА: {prd[0][6]}₽</b>\n<b>🔢 КОЛ-ВО: {logs_len}</b>\n\n<b>📄 ОПИСАНИЕ</b>: {prd[0][2]}', reply_markup=await user.get_product(prd_id=prd[0][0]), parse_mode="HTML")
    await call.message.delete()
    await call.message.answer_photo(photo=prd[0][3], caption=f'<b>🏷 {prd[0][1]}</b>\n\n<b>💎 ЦЕНА: {prd[0][6]}₽</b>\n<b>🔢 КОЛ-ВО: {logs_len}</b>\n\n<b>📄 ОПИСАНИЕ</b>: {prd[0][2]}', reply_markup=await user.get_product(prd_id=prd[0][0]), parse_mode="HTML")

@dp.callback_query(F.data[:18] == 'open_back_catalog_')
async def open_back_catalog(call: types.CallbackQuery):
    await call.message.delete()
    req=call.data[18:]
    if req == '0':
        await call.message.answer('Выбирай что надо', reply_markup=await user.get_catalog(req='0'))
        return
    ctg=await db.get_catalog(ctg_id=req)
    if ctg[0][3] == '0':
        return await call.message.answer(f'{ctg[0][2]}', reply_markup=await user.get_catalog(req=req), parse_mode="HTML")
    await call.answer_photo(photo=cfg[0][3], caption=f'{ctg[0][2]}', reply_markup=await user.get_catalog(req=req), parse_mode="HTML")

@dp.callback_query(F.data[:12] == 'buy_product_')
async def buy_product(call: types.CallbackQuery, state: FSMContext):
    if await check_spam(user_id=call.from_user.id):
        return await call.answer('🕓 Подождите')
    prd_id=call.data[12:]
    prd=await db.get_product(prd_id=prd_id)
    logs=await db.get_log(prd_id=prd[0][0])

    if prd[0][5]:
        balance=(await db.get_dataUser(user_id=call.from_user.id))[0][1]
        if prd[0][6] <= balance:
            await db.take_balance(prd[0][6], user_id=call.from_user.id)
            await call.message.answer(prd[0][7])
            await call.message.delete()
            id_history=await db.add_history(typee='product', product=prd[0][1], logs=prd[0][7], summ=prd[0][6], user_id=call.from_user.id)
            PATH='data/settings.json'
            data_json=json.load((open(PATH, 'r', encoding='UTF-8')))
            if data_json['nofication']['buy']:
                await nofication_pay(ID=call.from_user.id, product=prd[0][1], balance=(await db.get_dataUser(user_id=call.from_user.id))[0][1], lens='Бесконечный товар', price=prd[0][6], id_history=id_history)
            return
        return await call.answer('❌ У вас не хватает средств', show_alert=True)

    if len(logs) <= 0:
        return await call.answer(text='🛡 Извините товар закончился\n😇 Скоро добавим\n🔄 Ожидайте', show_alert=True)
    await call.message.delete()
    await state.set_state(product_user_state.lens_product)
    msg=await call.message.answer(text='<b>Сколько вы желайте приобрести товара</b>', reply_markup=await user.get_back_product(prd_id=prd_id), parse_mode="HTML")
    await state.update_data(prd_id=prd_id, msg_id=msg.message_id)
    

@dp.message(product_user_state.lens_product)
async def enter_len(message: types.Message, state: FSMContext):
    await message.delete()
    if await check_spam(user_id=message.from_user.id):
        return await message.answer('Подождите 🕘')
    try:
        lens=int(message.text)
    except:
        return
    data=await state.update_data()
    logs=await db.get_log(prd_id=data['prd_id'])
    if not len(logs) >= lens:
        await bot.delete_message(chat_id=message.from_user.id, message_id=data['msg_id'])
        prd=await db.get_product(prd_id=data['prd_id'])
        logs_len=len(await db.get_log(prd_id=prd[0][0])) if not prd[0][5] else '∞'
        if prd[0][3] == '0':
             await message.answer(f'<b>❗️ НЕКОРРЕКТНОЕ КОЛИЧЕСТВО\n\n🏷 {prd[0][1]}\n💎 ЦЕНА: {prd[0][6]}₽\n🔢 КОЛ-ВО: {logs_len}\n\n📄 ОПИСАНИЕ</b>: {prd[0][2]}', reply_markup=await user.get_product(prd_id=prd[0][0]), parse_mode="HTML")
        else:
            await message.answer_photo(photo=prd[0][3], caption=f'<b>❗️ НЕКОРРЕКТНОЕ КОЛИЧЕСТВО\n\n🏷 {prd[0][1]}\n💎 ЦЕНА: {prd[0][6]}₽\n🔢 КОЛ-ВО: {logs_len}\n\n📄 ОПИСАНИЕ</b>: {prd[0][2]}', reply_markup=await user.get_product(prd_id=prd[0][0]), parse_mode="HTML")
        return await state.clear()

    balance=(await db.get_dataUser(user_id=message.from_user.id))[0][1]
    prd=await db.get_product(prd_id=data['prd_id'])
    if prd[0][6] <= balance:
        await db.take_balance(prd[0][6], user_id=message.from_user.id)
        await bot.delete_message(chat_id=message.from_user.id, message_id=data['msg_id'])
        if prd[0][7] != '0':
            await message.answer(prd[0][7])
        text_logs=str()
        print(1)
        for i in range(0, lens):
            text_logs+=f'{i+1}: {logs[0][0]}\n'
            try:
                await db.del_log(prd_id=logs[0][0], item='log_name')
            except:
                pass
            logs=await db.get_log(prd_id=data['prd_id'])
        id_history=await db.add_history(typee='product', product=prd[0][1], logs=text_logs, summ=prd[0][6], user_id=message.from_user.id)
        PATH='data/settings.json'
        data_json=json.load((open(PATH, 'r', encoding='UTF-8')))
        if data_json['nofication']['buy']:
            await nofication_pay(ID=message.from_user.id, product=prd[0][1], balance=(await db.get_dataUser(user_id=message.from_user.id))[0][1], lens=lens, price=prd[0][6]*lens, id_history=id_history)
        await message.answer(text_logs)
    else:
        if prd[0][3] == '0':
             await message.answer(f'<b>❗️ НЕДОСТАТОЧНО СРЕДСТВ\n💎 Пополните баланс в профиле\n\n🏷 {prd[0][1]}\n💎 ЦЕНА: {prd[0][6]}₽\n🔢 КОЛ-ВО: {len(logs)}\n\n📄 ОПИСАНИЕ</b>: {prd[0][2]}', reply_markup=await user.get_product(prd_id=prd[0][0]), parse_mode="HTML")
        else:
            await message.answer_photo(photo=prd[0][3], caption=f'<b>❗️ НЕДОСТАТОЧНО СРЕДСТВ\n💎 Пополните баланс в профиле\n\n🏷 {prd[0][1]}\n💎 ЦЕНА: {prd[0][6]}₽\n🔢 КОЛ-ВО: {len(logs)}\n\n📄 ОПИСАНИЕ</b>: {prd[0][2]}', reply_markup=await user.get_product(prd_id=prd[0][0]), parse_mode="HTML")
        return await state.clear()

    await state.clear()

