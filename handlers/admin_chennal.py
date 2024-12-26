from loader import dp, bot, cfg
from core.routers import admin_router
from aiogram import types, F
from keyb import admin
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from data import db

class add_chennal_state(StatesGroup):
    message_forward=State()

@admin_router.callback_query(F.data == 'chennal_open')
async def chennal_menu(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(text='<b>⚙️ Здесь ты можешь настроить каналы\n❔ Проверка на подписку на канал\n🗑 Нажми на канал что бы его удалить</b>', reply_markup=await admin.get_chennal_menu(), parse_mode="HTML")

@admin_router.callback_query(F.data == 'add_chennal_admin')
async def add_call_chenal(call: types.CallbackQuery, state: FSMContext):
    back_main=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='🔙', callback_data='chennal_open')]])
    me=await bot.get_me()
    msg=await call.message.edit_text(text=f'<b>🤖 Добавь @{me.username} в админы\n↪️ Перешли любое сообщение с канала</b>', reply_markup=back_main, parse_mode="HTML")
    await state.set_state(add_chennal_state.message_forward)
    await state.update_data(msg_id=msg.message_id)

@admin_router.message(add_chennal_state.message_forward)
async def get_forward_message(message: types.Message, state: FSMContext):
    await message.delete()
    if message.forward_from_chat:
        try:
            await bot.get_chat_member(chat_id=message.forward_from_chat.id, user_id=cfg.admin_id)
            chennal=await bot.get_chat(chat_id=message.forward_from_chat.id)
            await db.add_chennal(message.forward_from_chat.id, chennal.invite_link)
            data=await state.update_data()
            await state.clear()
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['msg_id'],  text='<b>✅ Канал добавлен\n⚙️ Здесь ты можешь настроить каналы\n❔ Проверка на подписку на канал</b>', reply_markup=await admin.get_chennal_menu(), parse_mode="HTML")
        except:
            pass

@admin_router.callback_query(F.data[:21] == 'delete_chennal_admin_')
async def dell_chennal(call: types.CallbackQuery):
    chennal_id=call.data[21:]
    chennal=await bot.get_chat(chat_id=chennal_id)
    await db.delete_chennal(chennal_id)
    await call.message.edit_text(text=f'<b>⚙️ Здесь ты можешь настроить каналы\n❔ Проверка на подписку на канал\n🗑 {chennal.full_name} удален</b>', reply_markup=await admin.get_chennal_menu(), parse_mode="HTML")