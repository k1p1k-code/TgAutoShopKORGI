
from core.routers import admin_router
from loader import dp
from aiogram import types, F
from keyb import admin 
from data import db
import asyncio

@admin_router.message(F.text == '/admin')
async def cmd_admin(message: types.Message, state):
    await state.clear()
    await message.answer(f'<b>🧑‍💻 Админа панель 🧑‍💻\n👤 Пользователей: {len(await db.get_allusers())} 👤</b>', reply_markup=await admin.admin_main_menu(), parse_mode="HTML")

@admin_router.callback_query(F.data == 'back_mine_admin')
async def back_mine_admin(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('<b>🧑‍💻 Админа панель 🧑‍💻</b>', reply_markup=await admin.admin_main_menu(), parse_mode="HTML")

