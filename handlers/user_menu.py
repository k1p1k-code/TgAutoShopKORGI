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
    await state.clear()
    try:
        await db.add_user(user_id=message.from_user.id)
        await bot.send_message(chat_id=cfg.admin_id, text=f'<b>Новый пользователь: <a href="tg://user?id={message.from_user.id}">{message.from_user.id}</a></b>', parse_mode="HTML")
    except:
        pass
    PATH='data/settings.json'
    data_json=json.load((open(PATH, 'r', encoding='UTF-8')))
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