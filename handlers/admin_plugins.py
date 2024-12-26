from core.routers import admin_router
from loader import dp, cfg
from aiogram import types, F
from keyb import admin 
from aiogram.fsm.context import FSMContext
from core.loader_plugins import plugins

@admin_router.callback_query(F.data == 'plugins_open')
async def open_search(call: types.CallbackQuery):
    await call.message.edit_text(text='<b>БОТ НЕ ЗАЩИЩЕН ОТ НЕ ДОБРО КАЧЕСТВЕННЫХ ПАГИНОВ</b>', reply_markup=await admin.get_plugins_menu(plugins), parse_mode="HTML")


@admin_router.callback_query(F.data[:23] == 'plagins_settings_admin_')
async def open_search(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    plugin=plugins.plagins_object[call.data[23:]]
    await call.message.edit_text(text=f'<b>🤖 Плагин: {call.data[23:]}\n\n🏷 Название: {plugin.name}\n👤 Создатель: {plugin.creator}</b>', reply_markup=await admin.get_plugin_settings(plugin), parse_mode="HTML")


