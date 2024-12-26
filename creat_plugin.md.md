# Это гайд по созданию плагинов

Начало

1. Открыть папку где лежит main.py в редакторе код
2. Создать файл в plugins с уникальным названием


## Работа с билдером

Создаем экземпляр класса ВАЖНО Main

``` python
from utils.plugins_biuld import BuildPlugin
Main=BuildPlugin(name='Инлайн поиск', creator='K1p1k', on_startup=start)
```

name - название плагина

creator - создатель

on_startup - функция при старте

keyboard - кнопки плагина они отбржаются в /admin Плагины -> название плагина 

Если с name, creater все понятно

То с on_startup и keyboard не очень

Его можно использовать для показа работы 

``` python
from utils.plugins_biuld import BuildPlugin

async def start():
    await bot.send_message(chat_id=cfg.admin_id, text='Inline mod work!')

Main=BuildPlugin(name='Инлайн поиск', creator='K1p1k', on_startup=start)
```


Что бы создать меню настройки плагина можно использовать kyboard

``` python
inline_kb_list = [
    [InlineKeyboardButton(text="Выключить плагин", callback_data='on_off_unicakplugins')],
    [InlineKeyboardButton(text="Мой тг", url='Ссылка')]
    
    ]
```

системы вкл\выкл надо делать самим


## Работа с loader

Давайте напишем обработчик для нашей клавиатуры

dp - работа с диспетчиром

bot - робота с ботом

cfg - конфиг юзера(токен бота, админ айди)

Так же я вам помог и создал apscheduler прям в loader

``` python
from loader import dp, bot, cfg

@dp.callback_query(F.data == 'on_off_unicakplugins')
async def work_plugin(call: types.CallbackQuery):
  await call.message.answer('Я работаю!')
```

Так же есть роутер для работы с админом(не надо делать проверки)

``` python
from core.routers import admin_router

@admin_router.callback_query(F.data == 'on_off_unicakplugins')
async def upload_backup_plagin(call: types.CallbackQuery):
  await call.message.answer('Я работаю только для админа!')
```

