from routers import admin_router
from loader import dp, bot, cfg
from aiogram import types, F
from keyb import admin 
import asyncio
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from data import db

class add_product(StatesGroup):
    name_product=State()
    price_product=State()
    description_product=State()
    buytext_product=State()
    photo_product=State()

class edit_product(StatesGroup):  
    edit_name=State()
    edit_description=State()
    edit_buytext=State()
    edit_price=State()
    edit_photo=State()
    
class logs(StatesGroup):
    add=State()

@admin_router.callback_query(F.data[:12] == 'add_product_')
async def add_catalog_base(call: types.CallbackQuery, state: FSMContext):
    req=call.data[12:]
    if req == '0':
        return await call.answer('❗️В корневой каталог❗️\n❌ Нельзя добавить товар ❌', show_alert=True)
    await call.message.delete()
    msg=await call.message.answer('<b>🏷 Назване товара</b>', reply_markup=await admin.close_catalog(photo=False, cap='p'), parse_mode="HTML")
    await state.update_data(req=req)
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(add_product.name_product)



@admin_router.message(add_product.name_product)
async def get_name_catalog(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    data=await state.get_data()
    await message.delete()
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['msg_id'], text='<b>💭 Цена товара</b>', reply_markup=await admin.close_catalog(photo=False, cap='p'), parse_mode="HTML")
    await state.set_state(add_product.price_product)

@admin_router.message(add_product.price_product)
async def get_sum_product(message: types.Message, state: FSMContext):
    await message.delete()
    try:
        price=int(message.text)
    except:
        return
    await state.update_data(price=price)
    data=await state.get_data()
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['msg_id'], text='<b>📄 Описание товара</b>', reply_markup=await admin.close_catalog(photo=False, cap='p'), parse_mode="HTML")
    await state.set_state(add_product.description_product)

@admin_router.message(add_product.description_product)
async def get_description_catalog(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    data=await state.get_data()
    await message.delete()
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['msg_id'], text='<b>🗞 Сообщение после покуки товара\nОтправьте 0 если не нужно</b>', reply_markup=await admin.close_catalog(photo=False, cap='p'), parse_mode="HTML")
    await state.set_state(add_product.buytext_product)

@admin_router.message(add_product.buytext_product)
async def get_description_catalog(message: types.Message, state: FSMContext):
    await state.update_data(buytext=message.text)
    data=await state.get_data()
    await message.delete()
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['msg_id'], text='<b>📷 Фото для товара</b>', reply_markup=await admin.close_catalog(photo=True, cap='p'), parse_mode="HTML")
    await state.set_state(add_product.photo_product)


@admin_router.message(F.content_type == types.ContentType.PHOTO, add_product.photo_product)
async def  get_photo_catalog(message: types.Message, state: FSMContext):
    data=await state.get_data()
    await message.delete()
    await db.add_product(name=data['name'], discription=data['description'], photo=message.photo[-1].file_id, req=data['req'], price=data['price'], buytext=data['buytext'])
    ctg=await db.get_catalog(ctg_id=data['req'])
    await state.clear()
    if ctg[0][3] == '0':
        return await message.answer(f'<b>🗄 Каталог: {ctg[0][1]}\n📄 Описание: {ctg[0][2]}</b>', reply_markup=await admin.admin_product_menu(req=data['req']), parse_mode="HTML")
    await message.answer_photo(photo=cfg[0][3], caption=f'<b>🗄 Каталог: {ctg[0][1]}\n📄 Описание: {ctg[0][2]}</b>', reply_markup=await admin.admin_product_menu(req=data['req']), parse_mode="HTML")

@admin_router.callback_query(F.data == 'no_photo_product')
async def no_photo_catalog(call: types.CallbackQuery, state: FSMContext):
    data=await state.get_data()
    await call.message.delete()
    await db.add_product(name=data['name'], discription=data['description'], photo=0, req=data['req'], price=data['price'], buytext=data['buytext'])
    ctg=await db.get_catalog(ctg_id=data['req'])
    await state.clear()
    if ctg[0][3] == '0':
        return await call.message.answer(f'<b>🗄 Каталог: {ctg[0][1]}\n📄 Описание: {ctg[0][2]}</b>', reply_markup=await admin.admin_product_menu(req=data['req']), parse_mode="HTML")
    await call.message.answer_photo(photo=ctg[0][3], caption=f'<b>🗄 Каталог: {ctg[0][1]}\n📄 Описание: {ctg[0][2]}</b>', reply_markup=await admin.admin_product_menu(req=data['req']), parse_mode="HTML")

@admin_router.callback_query(F.data[:19] == 'edit_product_admin_')
async def edit_catalog_admin(call: types.CallbackQuery):
    prd_id=call.data[19:]
    data=await db.get_product(prd_id=prd_id)
    await call.message.delete()
    
    if data[0][3] == '0':
        await call.message.answer(f'<b>🗄 Товар: {data[0][1]}\n💭 Цена: {data[0][6]}₽\n📄 Описание: {data[0][2]}\n🗞 Текст после покупки: {data[0][7]}</b>', reply_markup=await admin.edit_product_admin(prd_id=prd_id), parse_mode='HTML')
        return
    await call.message.answer_photo(photo=data[0][3], caption=f'<b>🗄 Товар: {data[0][1]}\n💭 Цена: {data[0][6]}₽\n📄 Описание: {data[0][2]}\n🗞 Текст после покупки: {data[0][7]}</b>', reply_markup=await admin.edit_product_admin(prd_id=prd_id), parse_mode='HTML')
    

@admin_router.callback_query(F.data[:21] == 'delete_product_admin_')
async def delete_catalog_admin(call: types.CallbackQuery):
    prd_id=call.data[21:]
    req=(await db.get_product(prd_id=prd_id))[0][4]
    data=await db.get_catalog(ctg_id=req)
    await db.delete_product(prd_id=prd_id)
    await call.message.delete()
    if data[0][3] == '0':
        await call.message.answer(f'<b>🗄 Каталог: {data[0][1]}\n📄 Описание: {data[0][2]}\n🗞 Текст после покупки: {data[0][7]}</b>', reply_markup=await admin.admin_product_menu(req=req), parse_mode="HTML")
        return
    await call.message.answer_photo(photo=data[0][3], caption=f'<b>🗄 Каталог: {data[0][1]}\n📄 Описание: {data[0][2]}\n🗞 Текст после покупки: {data[0][7]}</b>', reply_markup=await admin.admin_product_menu(req=req), parse_mode="HTML")


############### EDIT NAME ###############
@admin_router.callback_query(F.data[:24] == 'edit_name_product_admin_')
async def edit_photo_catalog_admin(call: types.CallbackQuery, state: FSMContext):
    prd_id=call.data[24:]
    await state.set_state(edit_product.edit_name)
    await call.message.delete()
    msg=await call.message.answer('<b>🏷 Пришли новое название 🏷</b>', reply_markup=await admin.close_catalog(photo=False, cap='p'), parse_mode="HTML")
    await state.update_data(prd_id=prd_id, msg_id=msg.message_id)


@admin_router.message(edit_product.edit_name)
async def replace_photo(message: types.Message, state: FSMContext):
    data=await state.get_data()
    await bot.delete_message(chat_id=message.from_user.id, message_id=data['msg_id'])
    await message.delete()
    await db.replace_product(item='product_name', edit=message.text, prd_id=data['prd_id'])
    data_prd=await db.get_product(prd_id=data['prd_id'])
    await state.clear()
    if data_prd[0][3] == '0':
        await message.answer(f'<b>🗄 Товар: {data_prd[0][1]}\n💭 Цена: {data_prd[0][6]}₽\n📄 Описание: {data_prd[0][2]}\n🗞 Текст после покупки: {data_prd[0][7]}</b>', reply_markup=await admin.edit_product_admin(prd_id=data['prd_id']), parse_mode='HTML')
        return
    await message.answer_photo(photo=data_prd[0][3], caption=f'<b>🗄 Товар: {data_prd[0][1]}\n💭 Цена: {data_prd[0][6]}₽\n📄 Описание: {data_prd[0][2]}\n🗞 Текст после покупки: {data_prd[0][7]}</b>', reply_markup=await admin.edit_product_admin(prd_id=data['prd_id']), parse_mode='HTML')

############### EDIT DESCRIPTION ###############
@admin_router.callback_query(F.data[:30] == 'edit_disciption_product_admin_')
async def edit_photo_catalog_admin(call: types.CallbackQuery, state: FSMContext):
    prd_id=call.data[30:]
    await state.set_state(edit_product.edit_description)
    await call.message.delete()
    msg=await call.message.answer('<b>🏷 Пришли новое описание 🏷</b>', reply_markup=await admin.close_catalog(photo=False, cap='p'), parse_mode="HTML")
    await state.update_data(prd_id=prd_id, msg_id=msg.message_id)

@admin_router.message(edit_product.edit_description)
async def replace_photo(message: types.Message, state: FSMContext):
    data=await state.get_data()
    await bot.delete_message(chat_id=message.from_user.id, message_id=data['msg_id'])
    await message.delete()
    await db.replace_product(item='product_discription', edit=message.text, prd_id=data['prd_id'])
    data_prd=await db.get_product(prd_id=data['prd_id'])
    await state.clear()
    if data_prd[0][3] == '0':
        await message.answer(f'<b>🗄 Товар: {data_prd[0][1]}\n💭 Цена: {data_prd[0][6]}₽\n📄 Описание: {data_prd[0][2]}\n🗞 Текст после покупки: {data_prd[0][7]}</b>', reply_markup=await admin.edit_product_admin(prd_id=data['prd_id']), parse_mode='HTML')
        return
    await message.answer_photo(photo=data_prd[0][3], caption=f'<b>🗄 Товар: {data_prd[0][1]}\n💭 Цена: {data_prd[0][6]}₽\n📄 Описание: {data_prd[0][2]}\n🗞 Текст после покупки: {data_prd[0][7]}</b>', reply_markup=await admin.edit_product_admin(prd_id=data['prd_id']), parse_mode='HTML')

############### EDIT TEXTBUY ###############
@admin_router.callback_query(F.data[:27] == 'edit_buytext_product_admin_')
async def edit_textbuy_product_admin(call: types.CallbackQuery, state: FSMContext):
    prd_id=call.data[27:]
    await state.set_state(edit_product.edit_buytext)
    await call.message.delete()
    msg=await call.message.answer('<b>🗞 Сообщение после покуки товара\nОтправьте 0 если не нужно</b>', reply_markup=await admin.close_catalog(photo=False, cap='p'), parse_mode="HTML")
    await state.update_data(prd_id=prd_id, msg_id=msg.message_id)

@admin_router.message(edit_product.edit_buytext)
async def replace_textbuy(message: types.Message, state: FSMContext):
    data=await state.get_data()
    await bot.delete_message(chat_id=message.from_user.id, message_id=data['msg_id'])
    await message.delete()
    await db.replace_product(item='product_textbuy', edit=message.text, prd_id=data['prd_id'])
    data_prd=await db.get_product(prd_id=data['prd_id'])
    await state.clear()
    if data_prd[0][3] == '0':
        await message.answer(f'<b>🗄 Товар: {data_prd[0][1]}\n💭 Цена: {data_prd[0][6]}₽\n📄 Описание: {data_prd[0][2]}\n🗞 Текст после покупки: {data_prd[0][7]}</b>', reply_markup=await admin.edit_product_admin(prd_id=data['prd_id']), parse_mode='HTML')
        return
    await message.answer_photo(photo=data_prd[0][3], caption=f'<b>🗄 Товар: {data_prd[0][1]}\n💭 Цена: {data_prd[0][6]}₽\n📄 Описание: {data_prd[0][2]}\n🗞 Текст после покупки: {data_prd[0][7]}</b>', reply_markup=await admin.edit_product_admin(prd_id=data['prd_id']), parse_mode='HTML')

############### EDIT PRICE ###############
@admin_router.callback_query(F.data[:25] == 'edit_price_product_admin_')
async def edit_price_product_admin(call: types.CallbackQuery, state: FSMContext):
    prd_id=call.data[25:]
    await state.set_state(edit_product.edit_price)
    await call.message.delete()
    msg=await call.message.answer('<b>💭 Пришли новою цену </b>', reply_markup=await admin.close_catalog(photo=False, cap='p'), parse_mode="HTML")
    await state.update_data(prd_id=prd_id, msg_id=msg.message_id)

@admin_router.message(edit_product.edit_price)
async def replace_price(message: types.Message, state: FSMContext):
    await message.delete()
    try:
        price=int(message.text)
    except:
        return
    data=await state.get_data()
    await bot.delete_message(chat_id=message.from_user.id, message_id=data['msg_id'])
    await db.replace_product(item='product_price', edit=price, prd_id=data['prd_id'])
    await state.clear()
    data_prd=await db.get_product(prd_id=data['prd_id'])
    if data_prd[0][3] == '0':
        await message.answer(f'<b>🗄 Товар: {data_prd[0][1]}\n💭 Цена: {data_prd[0][6]}₽\n📄 Описание: {data_prd[0][2]}\n🗞 Текст после покупки: {data_prd[0][7]}</b>', reply_markup=await admin.edit_product_admin(prd_id=data['prd_id']), parse_mode='HTML')
        return
    await message.answer_photo(photo=data_prd[0][3], caption=f'<b>🗄 Товар: {data_prd[0][1]}\n💭 Цена: {data_prd[0][6]}₽\n📄 Описание: {data_prd[0][2]}\n🗞 Текст после покупки: {data_prd[0][7]}</b>', reply_markup=await admin.edit_product_admin(prd_id=data['prd_id']), parse_mode='HTML')

############### EDIT PHOTO ###############
@admin_router.callback_query(F.data[:25] == 'edit_photo_product_admin_')
async def edit_photo_product_admin(call: types.CallbackQuery, state: FSMContext):
    prd_id=call.data[25:]
    await state.set_state(edit_product.edit_photo)
    await call.message.delete()
    msg=await call.message.answer('<b>📷 Пришли новое фото 📷</b>', reply_markup=await admin.close_catalog(photo=False, cap='p'), parse_mode="HTML")
    await state.update_data(prd_id=prd_id, msg_id=msg.message_id)

@admin_router.message(edit_product.edit_photo, F.content_type == types.ContentType.PHOTO)
async def edit_replace_photo(message: types.Message, state: FSMContext):
    data=await state.get_data()
    await bot.delete_message(chat_id=message.from_user.id, message_id=data['msg_id'])
    await message.delete()
    await db.replace_product(item='product_photo', edit=message.photo[-1].file_id, prd_id=data['prd_id'])
    data_prd=await db.get_product(prd_id=data['prd_id'])
    await message.answer_photo(photo=data_prd[0][3], caption=f'<b>🗄 Товар: {data_prd[0][1]}\n💭 Цена: {data_prd[0][6]}₽\n📄 Описание: {data_prd[0][2]}\n🗞 Текст после покупки: {data_prd[0][7]}</b>', reply_markup=await admin.edit_product_admin(prd_id=data['prd_id']), parse_mode='HTML')
    await state.clear()


############### DEL PHOTO ###############
@admin_router.callback_query(F.data[:28] == 'edit_delphoto_product_admin_')
async def edit_delphoto_catalog_admin(call: types.CallbackQuery):
    prd_id=call.data[28:]
    data_prd=await db.get_product(prd_id=prd_id)
    if data_prd[0][3] == '0':
        return await call.answer('❌ Фото и так нет', show_alert=True)
    await call.message.delete()
    await db.replace_product(item='product_photo', edit=0, prd_id=prd_id)
    await call.message.answer(f'<b>🗄 Товар: {data_prd[0][1]}\n💭 Цена: {data_prd[0][6]}₽\n📄 Описание: {data_prd[0][2]}\n🗞 Текст после покупки: {data_prd[0][7]}</b>', reply_markup=await admin.edit_product_admin(prd_id=prd_id), parse_mode='HTML')

############### ON OFF INFINITY ###############
@admin_router.callback_query(F.data[:28] == 'edit_infinity_product_admin_')
async def edit_onoff_infinity_admin(call: types.CallbackQuery):
    prd_id=call.data[28:]
    data_prd=await db.get_product(prd_id=prd_id)
    if data_prd[0][5] == 1:
        await db.replace_product(item='product_infinity', edit=0, prd_id=prd_id)
    elif data_prd[0][5] == 0:
        await db.replace_product(item='product_infinity', edit=1, prd_id=prd_id)
        await call.answer(text='⚠️ В режиме бесконечность\n⚠️ Выдаеться "текст после покупки"', show_alert=True)
    await call.message.delete()
    if data_prd[0][3] == '0':
        await call.message.answer(f'<b>🗄 Товар: {data_prd[0][1]}\n💭 Цена: {data_prd[0][6]}₽\n📄 Описание: {data_prd[0][2]}\n🗞 Текст после покупки: {data_prd[0][7]}</b>', reply_markup=await admin.edit_product_admin(prd_id=prd_id), parse_mode='HTML')
        return
    await call.message.answer_photo(photo=data_prd[0][3], caption=f'<b>🗄 Товар: {data_prd[0][1]}\n💭 Цена: {data_prd[0][6]}₽\n📄 Описание: {data_prd[0][2]}\n🗞 Текст после покупки: {data_prd[0][7]}</b>', reply_markup=await admin.edit_product_admin(prd_id=prd_id), parse_mode='HTML')


############### ADD LOG PRODUCT ###############
@admin_router.callback_query(F.data[:22] == 'add_log_product_admin_')
async def add_logs_admin(call: types.CallbackQuery, state: FSMContext):
    prd_id=call.data[22:]
    await state.set_state(logs.add)
    await call.message.delete()
    msg=await call.message.answer('<b>🗞 Отправь логи 🗞\n❗️ Каждый лог начинай с новый строки ❗️</b>', reply_markup=await admin.close_catalog(photo=False, cap='p'), parse_mode='HTML')
    await state.update_data(prd_id=prd_id, msg_id=msg.message_id)
    
@admin_router.message(logs.add)
async def append_logs_admin(message: types.Message, state: FSMContext):
    data=await state.update_data()
    for i in message.text.split('\n'):
        await db.add_log(log=i, prd_id=data['prd_id'])
    data_prd=await db.get_product(prd_id=data['prd_id'])
    logs=list()
    for i,n in await db.get_log(prd_id=data['prd_id']):
        logs.append(i)
    await db.replace_product(item='product_infinity', edit=0, prd_id=data['prd_id'])
    if data_prd[0][3] == '0':
        await message.answer(f'Логи: {logs}\n\n<b>🗄 Товар: {data_prd[0][1]}\n💭 Цена: {data_prd[0][6]}₽\n📄 Описание: {data_prd[0][2]}\n🗞 Текст после покупки: {data_prd[0][7]}</b>', reply_markup=await admin.edit_product_admin(prd_id=data['prd_id']), parse_mode='HTML')
        return
    await message.answer_photo(photo=data_prd[0][3], caption=f'Логи: {logs}\n\n<b>🗄 Товар: {data_prd[0][1]}\n💭 Цена: {data_prd[0][6]}₽\n📄 Описание: {data_prd[0][2]}\n🗞 Текст после покупки: {data_prd[0][7]}</b>', reply_markup=await admin.edit_product_admin(prd_id=data['prd_id']), parse_mode='HTML')

############### DELETE LOG PRODUCT ###############
@admin_router.callback_query(F.data[:22] == 'del_log_product_admin_')
async def add_logs_admin(call: types.CallbackQuery):
    await db.del_log(prd_id=call.data[22:])
    await call.answer(text='✅ Логи удалены ✅', show_alert=True)

############### SHOW LOG PRODUCT ###############
@admin_router.callback_query(F.data[:23] == 'show_log_product_admin_')
async def show_logs_admin(call: types.CallbackQuery):
    prd_id=call.data[23:]
    data_prd=await db.get_product(prd_id=prd_id)
    logs=list()
    for i,n in await db.get_log(prd_id=prd_id):
        logs.append(i)
    await call.message.delete()
    if data_prd[0][3] == '0':
        await call.message.answer(f'Логи: {logs}\n\n<b>🗄 Товар: {data_prd[0][1]}\n💭 Цена: {data_prd[0][6]}₽\n📄 Описание: {data_prd[0][2]}\n🗞 Текст после покупки: {data_prd[0][7]}</b>', reply_markup=await admin.edit_product_admin(prd_id=prd_id), parse_mode='HTML')
        return
    await call.message.answer_photo(photo=data_prd[0][3], caption=f'Логи: {logs}\n\n<b>🗄 Товар: {data_prd[0][1]}\n💭 Цена: {data_prd[0][6]}₽\n📄 Описание: {data_prd[0][2]}\n🗞 Текст после покупки: {data_prd[0][7]}</b>', reply_markup=await admin.edit_product_admin(prd_id=prd_id), parse_mode='HTML')
