from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import db

back_mine=InlineKeyboardButton(text="🔙 Назад в меню", callback_data='back_mine')

back_profile=[[InlineKeyboardButton(text="🔙", callback_data='back_profile')]]

async def user_main_menu():
    inline_kb_list = [
        [InlineKeyboardButton(text="🏪 Товары", callback_data='open_main_product_0'), InlineKeyboardButton(text="👤 Профиль", callback_data='open_profile')],
        [InlineKeyboardButton(text="🆘 Поддержка", callback_data='open_help')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def get_catalog(req):
    inline_kb_list=list()
    data_сtg=await db.get_dataCatalog()
    data_prd=await db.get_dataProduct()
    for i in data_сtg:
        if i[4] == req:
            inline_kb_list.append([InlineKeyboardButton(text=f'{i[1]}', callback_data=f'open_catalog_user_{i[0]}')
                                ])
    for i in data_prd:
        if i[4] == req:
            infinity=(await db.get_product(prd_id=i[4]))[0][5]
            len_logs=len(await db.get_log(prd_id=i[4])) if infinity == 0 else '∞'
            inline_kb_list.append([InlineKeyboardButton(text=f'{i[1]} | {i[6]}₽ | КОЛ-ВО: {len_logs}', callback_data=f'open_product_user_{i[0]}')
                                ])
    if int(req) == 0:
        inline_kb_list.append([back_mine])
    else:
        back_ctg=(await db.get_catalog(ctg_id=req))[0][4]                       
        inline_kb_list.append([InlineKeyboardButton(text='◀️', callback_data=f'open_back_catalog_{back_ctg}'), back_mine])
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def user_profile_menu():
    inline_kb_list = [
        [InlineKeyboardButton(text="💰 Пополнить", callback_data='start_pay')],
        [InlineKeyboardButton(text="🗄 Мои покупки", callback_data='my_buyer')],
        #[InlineKeyboardButton(text="🤑 Реф. система", callback_data='open_referal')],
        [back_mine]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def user_ch_syspay(summ):
    inline_kb_list=list()
    ''.replace('lolz', '🟢 LOLZ').replace('yoomoney', '🟣  YOOMONEY').replace('cryptobot', '💎 CryptoBot')
    pay_data=await db.get_dataPay()
    for i in pay_data:
        if i[1]:
            inline_kb_list.append([InlineKeyboardButton(text=i[0].replace('lolz', '🟢 LOLZ').replace('yoomoney', '🟣  YOOMONEY').replace('cryptobot', '💎 CryptoBot'), callback_data=f'pay_profile_{i[0]}_{summ}')])

    inline_kb_list.append(back_profile[0])

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def pay_check(pay, comment, link, summ):
    inline_kb_list = [
        [InlineKeyboardButton(text="🔗 Перейте к оплате", url=link)],
        [InlineKeyboardButton(text="🔄 Проверить", callback_data=f'pay_check_profile_{comment}_{pay}_{summ}')],
        back_profile[0]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def get_product(prd_id):
    back_ctg=(await db.get_product(prd_id=prd_id))[0][4]  
    inline_kb_list = [
        [InlineKeyboardButton(text="💎 Купить", callback_data=f'buy_product_{prd_id}')],
        [InlineKeyboardButton(text='◀️', callback_data=f'open_back_catalog_{back_ctg}'), back_mine]

    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def get_back_product(prd_id):
    back_ctg=(await db.get_product(prd_id=prd_id))[0][4]    
    inline_kb_list = [
        [InlineKeyboardButton(text='◀️', callback_data=f'open_back_catalog_{back_ctg}'), back_mine]

    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)