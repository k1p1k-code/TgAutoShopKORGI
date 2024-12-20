from routers import admin_router
from loader import bot, dp
from aiogram import types, F
from keyb import admin 
import asyncio
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from data import db

class add_catalog(StatesGroup):
    name_catalog=State()
    description_catalog=State()
    photo_catalog=State()

class edit_catalog(StatesGroup):
    edit_photo=State()
    edit_name=State()
    edit_description=State()

class add_product(StatesGroup):
    name_catalog=State()
    description_catalog=State()
    photo_catalog=State()

@admin_router.callback_query(F.data == 'open_catalog_admin_0')
async def open_katalog_admin(call: types.CallbackQuery):
    await call.message.edit_text('<b>🧑‍💻 Редактор товаров 🧑‍💻</b>', reply_markup=await admin.admin_product_menu(req='0'), parse_mode="HTML")

@admin_router.callback_query(F.data[:19] == 'open_catalog_admin_')
async def open_custom_catalog(call: types.CallbackQuery):
    ctg_id=call.data[19:]
    data=await db.get_catalog(ctg_id=ctg_id)
    await call.message.delete()
    if data[0][3] == '0':
        await call.message.answer(f'<b>🗄 Каталог: {data[0][1]}\n📄 Описание: {data[0][2]}</b>', reply_markup=await admin.admin_product_menu(req=ctg_id), parse_mode="HTML")
        return
    await call.message.answer_photo(photo=data[0][3], caption=f'<b>🗄 Каталог: {data[0][1]}\n📄 Описание: {data[0][2]}</b>', reply_markup=await admin.admin_product_menu(req=ctg_id), parse_mode="HTML")

@admin_router.callback_query(F.data == 'colse_create_product_admin')
async def colse_create_product_admin(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text('<b>🧑‍💻 Редактор товаров 🧑‍💻</b>', reply_markup=await admin.admin_product_menu(req='0'), parse_mode="HTML")
    await state.clear()

@dp.callback_query(F.data[:12] == 'add_catalog_')
async def add_catalog_base(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    msg=await call.message.answer('<b>🏷 Назване каталога</b>', reply_markup=await admin.close_catalog(photo=False, cap='c'), parse_mode="HTML")
    await state.update_data(req=call.data[12:])
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(add_catalog.name_catalog)

@dp.message(add_catalog.name_catalog)
async def get_name_catalog(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    data=await state.get_data()
    await message.delete()
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['msg_id'], text='<b>📄 Описание каталога</b>', reply_markup=await admin.close_catalog(photo=False, cap='c'), parse_mode="HTML")
    await state.set_state(add_catalog.description_catalog)


@dp.message(add_catalog.description_catalog)
async def get_description_catalog(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    data=await state.get_data()
    await message.delete()
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['msg_id'], text='<b>📷 Фото для каталога</b>', reply_markup=await admin.close_catalog(photo=True, cap='c'), parse_mode="HTML")
    await state.set_state(add_catalog.photo_catalog)

@dp.message(F.content_type == types.ContentType.PHOTO, add_catalog.photo_catalog)
async def  get_photo_catalog(message: types.Message, state: FSMContext):
    data=await state.get_data()
    ctg=await db.get_dataCatalog()
    ctg_id=str(1 if len(ctg) == 0 else int(ctg[-1][0])+1)
    await message.delete()
    await db.add_catalog(name=data['name'], discription=data['description'], photo=message.photo[-1].file_id, req=data['req'])
    await message.answer_photo(photo=message.photo[-1].file_id, caption=f'<b>🗄 Каталог: {data['name']}\n📄 Описание: {data['description']}</b>', reply_markup=await admin.admin_product_menu(req=ctg_id), parse_mode="HTML")
    await state.clear()

@dp.callback_query(F.data == 'no_photo_catalog')
async def no_photo_catalog(call: types.CallbackQuery, state: FSMContext):
    data=await state.get_data()
    ctg=await db.get_dataCatalog()
    ctg_id=str(1 if len(ctg) == 0 else int(ctg[-1][0])+1)
    await call.message.delete()
    await db.add_catalog(name=data['name'], discription=data['description'], photo=0, req=data['req'])
    await call.message.answer(f'<b>🗄 Каталог: {data['name']}\n📄 Описание: {data['description']}</b>', reply_markup=await admin.admin_product_menu(req=ctg_id), parse_mode="HTML")
    await state.clear()
    

@dp.callback_query(F.data[:19] == 'edit_catalog_admin_')
async def edit_catalog_admin(call: types.CallbackQuery):
    ctg_id=call.data[19:]
    data=await db.get_catalog(ctg_id=ctg_id)
    await call.message.delete()
    if data[0][3] == '0':
        await call.message.answer(f'<b>🗄 Каталог: {data[0][1]}\n📄 Описание: {data[0][2]}</b>', reply_markup=await admin.edit_catalog_admin(ctg_id=ctg_id), parse_mode='HTML')
        return
    await call.message.answer_photo(photo=data[0][3], caption=f'<b>🗄 Каталог: {data[0][1]}\n📄 Описание: {data[0][2]}</b>', reply_markup=await admin.edit_catalog_admin(ctg_id=ctg_id), parse_mode='HTML')
    


@dp.callback_query(F.data[:21] == 'delete_catalog_admin_')
async def delete_catalog_admin(call: types.CallbackQuery):
    ctg_id=call.data[21:]
    data=await db.get_catalog(ctg_id=ctg_id)
    await call.message.delete()
    await call.message.answer(f'Вы действитель хотите удалить категорию❓\n{data[0][1]}', reply_markup=await admin.accept_delete(ctg_id=ctg_id))

@dp.callback_query(F.data[:29] == 'deletre_accept_catalog_admin_')
async def deletre_accept_catalog_admin(call: types.CallbackQuery):
    ctg_id=call.data[29:]
    allctg=await db.get_dataCatalog()

    ctgs_delete=list()
    for i in allctg:
        if i[4] == ctg_id:
            ctgs_delete.append(i[0])
    
    for i in ctgs_delete:
        await db.delete_catalog(i)
    await db.delete_catalog(ctg_id)
    await call.message.edit_text('<b>🧑‍💻 Редактор товаров 🧑‍💻\n🗑 Успешно удалено 🗑</b>', reply_markup=await admin.admin_product_menu(req='0'), parse_mode="HTML")



@dp.callback_query(F.data[:24] == 'edit_name_catalog_admin_')
async def edit_photo_catalog_admin(call: types.CallbackQuery, state: FSMContext):
    ctg_id=call.data[24:]
    await state.set_state(edit_catalog.edit_name)
    await call.message.delete()
    msg=await call.message.answer('<b>🏷 Пришли новое название 🏷</b>', reply_markup=await admin.close_catalog(photo=False, cap='c'), parse_mode="HTML")
    await state.update_data(ctg_id=ctg_id, msg_id=msg.message_id)

@dp.message(edit_catalog.edit_name)
async def replace_photo(message: types.Message, state: FSMContext):
    data=await state.get_data()
    await bot.delete_message(chat_id=message.from_user.id, message_id=data['msg_id'])
    await message.delete()
    await db.replace_catalog(item='catolog_name', edit=message.text, ctg_id=data['ctg_id'])
    data_ctg=await db.get_catalog(ctg_id=data['ctg_id'])
    await state.clear()
    if data_ctg[0][3] == '0':
        return await message.answer(f'<b>🗄 Каталог: {data_ctg[0][1]}\n📄 Описание: {data_ctg[0][2]}</b>', reply_markup=await admin.edit_catalog_admin(ctg_id=data['ctg_id']), parse_mode='HTML')
    await message.answer_photo(photo=data_ctg[0][3], caption=f'<b>🗄 Каталог: {data_ctg[0][1]}\n📄 Описание: {data_ctg[0][2]}</b>', reply_markup=await admin.edit_catalog_admin(ctg_id=data['ctg_id']), parse_mode='HTML')
    
@dp.callback_query(F.data[:30] == 'edit_disciption_catalog_admin_')
async def edit_photo_catalog_admin(call: types.CallbackQuery, state: FSMContext):
    ctg_id=call.data[30:]
    await state.set_state(edit_catalog.edit_description)
    await call.message.delete()
    msg=await call.message.answer('<b>🏷 Пришли новое описание 🏷</b>', reply_markup=await admin.close_catalog(photo=False, cap='c'), parse_mode="HTML")
    await state.update_data(ctg_id=ctg_id, msg_id=msg.message_id)

@dp.message(edit_catalog.edit_description)
async def replace_photo(message: types.Message, state: FSMContext):
    data=await state.get_data()
    await bot.delete_message(chat_id=message.from_user.id, message_id=data['msg_id'])
    await message.delete()
    await db.replace_catalog(item='catalog_discription', edit=message.text, ctg_id=data['ctg_id'])
    data_ctg=await db.get_catalog(ctg_id=data['ctg_id'])
    await state.clear()
    if data_ctg[0][3] == '0':
        return await message.answer(f'<b>🗄 Каталог: {data_ctg[0][1]}\n📄 Описание: {data_ctg[0][2]}</b>', reply_markup=await admin.edit_catalog_admin(ctg_id=data['ctg_id']), parse_mode='HTML')
    await message.answer_photo(photo=data_ctg[0][3], caption=f'<b>🗄 Каталог: {data_ctg[0][1]}\n📄 Описание: {data_ctg[0][2]}</b>', reply_markup=await admin.edit_catalog_admin(ctg_id=data['ctg_id']), parse_mode='HTML')

@dp.callback_query(F.data[:25] == 'edit_photo_catalog_admin_')
async def edit_photo_catalog_admin(call: types.CallbackQuery, state: FSMContext):
    ctg_id=call.data[25:]
    await state.set_state(edit_catalog.edit_photo)
    await call.message.delete()
    msg=await call.message.answer('<b>📷 Пришли новое фото 📷</b>', reply_markup=await admin.close_catalog(photo=False, cap='c'), parse_mode="HTML")
    await state.update_data(ctg_id=ctg_id, msg_id=msg.message_id)

@dp.message(edit_catalog.edit_photo, F.content_type == types.ContentType.PHOTO)
async def replace_photo(message: types.Message, state: FSMContext):
    data=await state.get_data()
    await bot.delete_message(chat_id=message.from_user.id, message_id=data['msg_id'])
    await message.delete()
    await db.replace_catalog(item='catalog_photo', edit=message.photo[-1].file_id, ctg_id=data['ctg_id'])
    data_ctg=await db.get_catalog(ctg_id=data['ctg_id'])
    await message.answer_photo(photo=data_ctg[0][3], caption=f'<b>🗄 Каталог: {data_ctg[0][1]}\n📄 Описание: {data_ctg[0][2]}</b>', reply_markup=await admin.edit_catalog_admin(ctg_id=data['ctg_id']), parse_mode='HTML')
    await state.clear()

@dp.callback_query(F.data[:28] == 'edit_delphoto_catalog_admin_')
async def edit_delphoto_catalog_admin(call: types.CallbackQuery):
    ctg_id=call.data[28:]
    data=await db.get_catalog(ctg_id=ctg_id)
    if data[0][3] == '0':
        return await call.answer('❌ Фото и так нет', show_alert=True)
    await call.message.delete()
    await db.replace_catalog(item='catalog_photo', edit=0, ctg_id=ctg_id)
    await call.message.answer(text=f'<b>🗄 Каталог: {data[0][1]}\n📄 Описание: {data[0][2]}</b>', reply_markup=await admin.edit_catalog_admin(ctg_id=ctg_id), parse_mode='HTML')
    