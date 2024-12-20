from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import db
import json


back_mine=InlineKeyboardButton(text="🔙", callback_data='back_mine_admin')

async def admin_main_menu():
    inline_kb_list = [
        [InlineKeyboardButton(text="🏪 Товары", callback_data='open_catalog_admin_0')],
        [InlineKeyboardButton(text="💳 Способы оплаты", callback_data='pay_menu_open')],
        [InlineKeyboardButton(text="🔍 Поиск", callback_data='search_menu_open')],
        [InlineKeyboardButton(text="📢 Рассылка", callback_data='mailing_start')],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data='settings_open')],
        [InlineKeyboardButton(text="🧩 Плагины", callback_data='plugins_open')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


async def admin_product_menu(req):
    inline_kb_list=list()
    data_ctg=await db.get_dataCatalog()
    data_prd=await db.get_dataProduct()
    for i in data_ctg:
        if i[4] == req:
            inline_kb_list.append([InlineKeyboardButton(text=f'K: {i[1]}', callback_data=f'open_catalog_admin_{i[0]}'),
                                InlineKeyboardButton(text='🗑', callback_data=f'delete_catalog_admin_{i[0]}'),
                                InlineKeyboardButton(text='✏️', callback_data=f'edit_catalog_admin_{i[0]}')
                                ])
    for i in data_prd:
        if i[4] == req:
            infinity=(await db.get_product(prd_id=i[4]))[0][5]
            len_logs=len(await db.get_log(prd_id=i[4])) if infinity == 0 else '∞'
            inline_kb_list.append([InlineKeyboardButton(text=f'Т: {i[1]} | КОЛ-ВО: {len_logs}', callback_data=f'edit_product_admin_{i[0]}'),
                                InlineKeyboardButton(text='🗑', callback_data=f'delete_product_admin_{i[0]}')
                                ])

    inline_kb_list.append([InlineKeyboardButton(text="➕ Добавить товар", callback_data=f'add_product_{req}')])    
    inline_kb_list.append([InlineKeyboardButton(text="➕➕ Добавить категорию", callback_data=f'add_catalog_{req}')])
    inline_kb_list.append([back_mine])
   
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def close_catalog(photo, cap):
    if cap == 'c':
        call='no_photo_catalog'
    elif cap == 'p':
        call='no_photo_product'
    inline_kb_list = [
        [InlineKeyboardButton(text="🔙", callback_data='colse_create_product_admin')]]
    if photo:
        inline_kb_list.append([InlineKeyboardButton(text="👁 Без фото", callback_data=call) if photo else None])
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def accept_delete(ctg_id):
    inline_kb_list = [
        [InlineKeyboardButton(text="🗑 Удалить", callback_data=f'deletre_accept_catalog_admin_{ctg_id}')],
        [back_mine]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def edit_catalog_admin(ctg_id):
    inline_kb_list = [
        [InlineKeyboardButton(text="🏷 Изменить название", callback_data=f'edit_name_catalog_admin_{ctg_id}'), 
        InlineKeyboardButton(text="📄 Изменить описание", callback_data=f'edit_disciption_catalog_admin_{ctg_id}')],

        [InlineKeyboardButton(text="📷 Изменить\добавить фото", callback_data=f'edit_photo_catalog_admin_{ctg_id}'),
         InlineKeyboardButton(text="📷 Удалить фото", callback_data=f'edit_delphoto_catalog_admin_{ctg_id}')],
         [back_mine]
         ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
    
async def edit_product_admin(prd_id):
    prd=await db.get_product(prd_id=prd_id)
    infinity='🔴' if prd[0][5] == 0 else '🟢'
    inline_kb_list = [
        [InlineKeyboardButton(text="🏷 Изменить название", callback_data=f'edit_name_product_admin_{prd_id}'), 
        InlineKeyboardButton(text="📄 Изменить описание", callback_data=f'edit_disciption_product_admin_{prd_id}')],
        [InlineKeyboardButton(text="🗞 Изменить текст после покупки", callback_data=f'edit_buytext_product_admin_{prd_id}')],
        [InlineKeyboardButton(text="💭 Изменить цену", callback_data=f'edit_price_product_admin_{prd_id}')],
        [InlineKeyboardButton(text="📷 Изменить\добавить фото", callback_data=f'edit_photo_product_admin_{prd_id}'),
         InlineKeyboardButton(text="📷 Удалить фото", callback_data=f'edit_delphoto_product_admin_{prd_id}')],
         [InlineKeyboardButton(text=f"♾ Бесконечность: {infinity}", callback_data=f'edit_infinity_product_admin_{prd_id}')],
         [InlineKeyboardButton(text="📥 Добавить логи товара", callback_data=f'add_log_product_admin_{prd_id}'),
           InlineKeyboardButton(text="📤 Удалить все логи товара", callback_data=f'del_log_product_admin_{prd_id}')],
        [InlineKeyboardButton(text="🗒 Показать логи", callback_data=f'show_log_product_admin_{prd_id}')],
         [back_mine]
         ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def close_pay(pay):
    inline_kb_list = [
        [InlineKeyboardButton(text="🔙", callback_data=f'colse_edit_pay_{pay}')]]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def admin_paysys_menu():
    inline_kb_list = [
        [InlineKeyboardButton(text="🟣Yoomoney🟣", callback_data='pay_open_admin_yoomoney')],
        [InlineKeyboardButton(text="🟢LOLZ🟢", callback_data='pay_open_admin_lolz')],
         [back_mine]
         ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def settings_pay(pay):
    pay_data=await db.get_pay(pay=pay)
    work='🔴' if pay_data[0][1] == 0  else '🟢'
    inline_kb_list = [
        [InlineKeyboardButton(text="🔐 Добавить/Изменить токен", callback_data=f'pay_edit_token_admin_{pay}')],
        [InlineKeyboardButton(text=f"🕹 Работает: {work}", callback_data=f'pay_edit_onoff_admin_{pay}')],
         [back_mine]
         ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


async def admin_search():
    inline_kb_list = [
        [InlineKeyboardButton(text="👤 Пользователей", callback_data='search_user'), InlineKeyboardButton(text="📦 Заказы", callback_data='search_payments')],
         [back_mine]
         ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def get_settings_user(user_id):
    isban= '🔒 Забанить' if  (await db.get_dataUser(user_id))[0][3] == 1 else '🔐 Разбанить'
    inline_kb_list = [
        [InlineKeyboardButton(text="🔁 Заменить количество денег", callback_data=f'user_edit_money_admin_{user_id}')],
        [InlineKeyboardButton(text=isban, callback_data=f'user_edit_ban_admin_{user_id}')],
        [InlineKeyboardButton(text=f'📜 История', callback_data=f'user_show_history_admin_{user_id}')],
         [InlineKeyboardButton(text='🔙', callback_data='search_menu_open')]
         ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

    switch_open

async def get_settings_menu():
    PATH='data/settings.json'
    data=json.load((open(PATH, 'r', encoding='UTF-8')))
    
    iswork='🔴 Выключить' if data['work'] == True else '🟢 Включить'
    inline_kb_list = [
        [InlineKeyboardButton(text=f"{iswork} бота", callback_data=f'onoff_bot_work_admin')],
        [InlineKeyboardButton(text='📖 Текста', callback_data='bot_text_menu_admin')],
         [back_mine]
         ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def get_texts_menu():
    inline_kb_list = [
        [InlineKeyboardButton(text="👋 Приветствие", callback_data='edit_text_hello_admin')],
        [InlineKeyboardButton(text="👤 Профиль", callback_data='edit_text_profile_admin')],
        [InlineKeyboardButton(text="🆘 Подержка", callback_data='edit_text_help_admin')],
         [InlineKeyboardButton(text='🔙', callback_data='settings_open')]
         ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def get_mailing(more_kb=list()):
    inline_kb_list = [
        [InlineKeyboardButton(text="⏹️ Добавить кнопку(url)", callback_data='mailing_add_button_admin')],
         [back_mine]
         ]
    for i in more_kb:
        inline_kb_list.append(i)
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def get_plugins_menu(plugins):
    inline_kb_list = list()
    
    for i in plugins.plagins:
        inline_kb_list.append([InlineKeyboardButton(text=i[:-3], callback_data=f'plagins_settings_admin_{i}')])
    inline_kb_list.append([back_mine])
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def get_plugin_settings(plugin):
    inline_kb_list = list()
    for i in plugin.keyboard:
        inline_kb_list.append(i)
    inline_kb_list.append([back_mine])
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)