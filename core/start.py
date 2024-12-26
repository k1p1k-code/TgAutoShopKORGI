import asyncio
from time import sleep
async def start_bot():
    from loader import bot, cfg, scheduler
    await bot.send_photo(chat_id=cfg.admin_id, photo='https://i.imgur.com/Lzch3s4.jpeg', caption='<b>🌟 Поставь звезду: https://github.com/k1p1k-code/TgAutoShopKORGI\n📬 Подпишись: @AutoShopKorgi\n🦠 Нашел баг: @createrb0t</b>', parse_mode="HTML")
    import os
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    import core.loader_plugins as loader_plugins
    from handlers import dp
    from data import db
    scheduler.start()
    for i in loader_plugins.on_startup:
        await i()
    me=await bot.me()
    await db.connect_db()
    print(f'\n\nБот запустился: @{me.username}')
    print(f'Ошибки баги: @AutoShopKorgi')
    print(f'Скачать: https://github.com/k1p1k-code/TgAutoShopKORGI')
    sleep(0.5)
    await dp.start_polling(bot)


def start():
    asyncio.run(start_bot())