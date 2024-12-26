from loader import dp, bot, cfg
from aiogram import types, F
from aiogram.filters import CommandStart
from keyb import user 
import json
import asyncio
from data import db
from datetime import datetime
from data.json_utils import get_texts

@dp.callback_query(F.data == 'back_mine')
async def back_main(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer((await get_texts())['start'].format(username=call.from_user.username,
                                                                  full_name=call.from_user.full_name,
                                                                  fist_name=call.from_user.first_name,
                                                                  id=call.from_user.id
    
    ), reply_markup=await user.user_main_menu(), parse_mode="HTML")

@dp.message(CommandStart())
async def cmd_start(message: types.Message, state):

    try:
        data_start=message.text.split()[1]
    except:
        data_start=False
    if data_start:
        if data_start[:6] == 'prd_id':
            prd=await db.get_product(prd_id=data_start.split('_')[2])
            logs_len=len(await db.get_log(prd_id=prd[0][0])) if not prd[0][5] else '∞'
            if prd[0][3] == '0':
                await message.answer(f'<b>🏷 {prd[0][1]}</b>\n\n<b>💎 ЦЕНА: {prd[0][6]}₽</b>\n<b>🔢 КОЛ-ВО: {logs_len}</b>\n\n<b>📄 ОПИСАНИЕ</b>: {prd[0][2]}', reply_markup=await user.get_product(prd_id=prd[0][0]), parse_mode="HTML")
            else:
                await message.answer_photo(photo=prd[0][3], caption=f'<b>🏷 {prd[0][1]}</b>\n\n<b>💎 ЦЕНА: {prd[0][6]}₽</b>\n<b>🔢 КОЛ-ВО: {logs_len}</b>\n\n<b>📄 ОПИСАНИЕ</b>: {prd[0][2]}', reply_markup=await user.get_product(prd_id=prd[0][0]), parse_mode="HTML")
    await state.clear()
    try:
        await db.add_user(user_id=message.from_user.id)
        await bot.send_message(chat_id=cfg.admin_id, text=f'<b>Новый пользователь: <a href="tg://user?id={message.from_user.id}">{message.from_user.id}</a></b>', parse_mode="HTML")
    except:
        pass
    no_sub=list()
    for i in await db.get_dataChennal():
        try:
            chennal_user=await bot.get_chat_member(chat_id=i[0], user_id=message.from_user.id)
        except:
            continue
        if chennal_user.status == 'left':
            no_sub.append(i[1])
    if no_sub:
        await bot.send_message(chat_id=message.from_user.id, text='<b>✅ Подпишись на каналы\n✅ Что бы воспользоваться ботом</b>', reply_markup=await user.get_chennal_sub(no_sub), parse_mode="HTML")
        return

    PATH='data/settings.json'
    await message.answer((await get_texts())['start'].format(username=message.from_user.username,
                                                             full_name=message.from_user.full_name,
                                                             fist_name=message.from_user.first_name,
                                                             id=message.from_user.id
    
    ), reply_markup=await user.user_main_menu(), parse_mode="HTML")




@dp.callback_query(F.data == 'open_help')
async def open_sos(call: types.CallbackQuery):
    back_main=types.InlineKeyboardMarkup(inline_keyboard=[[user.back_mine]])
    admin=await bot.get_chat(cfg.admin_id)
    creator='@'+admin.username
    await call.message.edit_text((await get_texts())['help'].format(username=call.from_user.username,
                                                                  full_name=call.from_user.full_name,
                                                                  fist_name=call.from_user.first_name,
                                                                  id=call.from_user.id,
                                                                  creator=creator
                                                                  ), reply_markup=back_main, parse_mode="HTML")