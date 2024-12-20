import asyncio

async def start_bot():
    from loader import bot, cfg, scheduler
    await bot.send_photo(chat_id=cfg.admin_id, photo='https://i.imgur.com/Lzch3s4.jpeg', caption='<b>🌟 Поставь звезду: https://github.com/k1p1k-code/TgAutoShopKORGI\n📬 Подпишись: @KorgiAutoShop\n🦠 Нашел баг: @createrb0t</b>', parse_mode="HTML")
    import os
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    import loader_plugins
    from handlers import dp
    from data import db
    scheduler.start()
    for i in loader_plugins.on_startup:
        await i()
    me=await bot.me()
    await db.connect_db()
    print(f'\n\nБот запустился: @{me.username}')
    print(f'Ошибки баги: @KorgiAutoShop')
    print(f'Сотруничество: @K1p1k')
    print(f'Скачать: https://github.com/k1p1k-code/TgAutoShopKORGI')

    await dp.start_polling(bot)


def start():
    asyncio.run(start_bot())