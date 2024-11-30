
# **Начало**
**1\. Скачать самого бота из [realease]([realese](https://github.com/k1p1k-code/TgAutoShopKORGI/releases))**

**2\. Открыть VS code или PyCharm в папке AutoShopByK1p1k**

**3\. Создать скрипт python в папке  ```plugins``` с уникальным названием**

# **Написание плагина**

**Выполним импорт билдера он дает возможно получить данные скрипта в саммого бот**

**```from utils.plugins_biuld import BuildPlugin```**

**Следующим действием мы должны создать экземляр класса обезательно Main**

``` python
Main=BuildPlugin(name='Мой первый плагин', creator='Вы', on_startup=start, keyboard=inline_kb_list)

```

**name: Название плагина**

**creator: Создатель**

**on_startup: функция которая будет запускаться сразу после старта бота или подзагрузки плагина**

**keyboard: указываем обезательно inline кнопки которые будут отображаться в меню плагина(кнопка возращение в главное меню автомотически добавляется)**

## **Обезательно сделать подгрузку pip**
**Это надо что бы не было ошибок при импорте плагина во время запущеного бота**

**Пример:**
``` python
#Инпортируем main из pip
from pip._internal.cli.main import main
try:
    #Если ошибки нет то импортируем
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    import apscheduler
except:
    #Если есть то загружаем нужный модуль и опять импортируем
    main(["install", "apscheduler"])
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    import apscheduler
```

# Прописать логику для  плагина

**Здесь все легко не нужно всего лишь базовые знания aiogram**

**Допустим я хочу что бы при команде "админ" выводились контакты админа**

**Примечание: эземпляр bot(Bot) и dp(Dispetcher) импортировать из loader**


``` python
from loader import dp

@dp.message(F.text.lower() == 'админ')
async def get_contact_admin(message: types.Message):
    await message.answer('Админ: @k1p1k')
```

# Итог 

``` python
from utils.plugins_biuld import BuildPlugin
from loader import dp
from aiogram import F
from aiogram import types

@dp.message(F.text.lower() == 'админ')
async def get_contact_admin(message: types.Message):
    await message.answer('Админ: @k1p1k')

Main=BuildPlugin(name='Give admin', creator='@k1p1k')

```

# **Давайте напишем пользный плагин**

**Примечание: данный плагин идет из коробки**


**Создадим плагин который будет нам присылать buckup базы и плагинов и так же его приминять**

**Нам нужен apscheduler для отправки buckup**

``` python
from pip._internal.cli.main import main
try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    import apscheduler
except:
    main(["install", "apscheduler"])
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    import apscheduler
```

**Создаем экземпляр**

``` python
# Определяем таймзону
TIMEZONE='Europe/Moscow'

#  scheduler для отправки сообщений в заплонированое время
scheduler=AsyncIOScheduler(timezone=TIMEZONE)
```

**Делаем билдер бекапа**
``` python
import os
import zipfile

class BuildBackup():
    def __init__(self):
        self.path='data/temp_bot/korgi.buckup'
        self.zipf = zipfile.ZipFile(self.path, 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk('data/'):
            for file in files:
                if file in ['DataBase.db', 'settings.json']:
                    self.zipf.write(os.path.join(root, file))

        for root, dirs, files in os.walk('plugins/'):
            for file in files:
                if file[-2:] == 'py':
                    self.zipf.write(os.path.join(root, file))        

    async def close(self):
        os.remove(self.path)
        self.zipf.close()
```

**Создаем кнопки для плагина**
``` python
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_kb_list = [
    [InlineKeyboardButton(text="📥 Загрузить бекап", callback_data=f'upload_backup_plagin')],
    [InlineKeyboardButton(text="🗃 Бекап", callback_data=f'send_backup_plagin')]
    
    ]
```

**Создаем функцию для отправки бекапа админу**
``` python
from aiogram.types.input_file import FSInputFile
from loader import bot, cfg

async def send_backup(callback):
    buckup=BuildBackup()
    document = FSInputFile(buckup.path)
    await bot.send_document(cfg.admin_id, document=document)
    await buckup.close()
```

**Создаем задачу для apscheduler**
``` python
from datetime import datetime

autobackup=scheduler.add_job(send_backup, trigger='cron', hour=datetime.now().hour, minute=datetime.now().minute+1, start_date=datetime.now(), kwargs={'callback' : types.CallbackQuery})
```

**Прописываем функцию для on_startup**

```python
async def start():
    scheduler.start()
```

**Экземпляр билдера**

``` python
Main=BuildPlugin(name='Автобэкап(встроенный)',
    creator='K1p1k',
    on_startup=start,
    keyboard=inline_kb_list
    )
```

**Регистарция кнопки бекап**
``` python
from loader import dp
#создаем хендлер
#не пугайтесь этот вы можете использовать обычный способ @dp.message
#это нужно что бы не писать вторый раз функцию send_backup
dp.callback_query.register(send_backup, F.data == 'send_backup_plagin')
```

**Пишем хендеры для приема бекапа**

``` python
#Нужен что бы определить название файла нужно для возращения в меню плагина и в общем получение название ФАЙЛА плагина
__file__.split('/')[-1]
``` 
___

``` python
#создание хендлера на обработку кнопки загрузки бекап
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import F
from data import db
from keyb import admin

class backupSTATE(StatesGroup):
    file=State()

@dp.callback_query(F.data == 'upload_backup_plagin')
async def upload_backup_plagin(call: types.CallbackQuery, state: FSMContext):
    back_main=types.InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙", callback_data=f'plagins_settings_admin_{__file__.split('/')[-1]}')]])
    await state.set_state(state=backupSTATE.file)
    msg=await call.message.edit_text('<b>❗️ Важно: база заменяется!\n📥 Отправь backup</b>', reply_markup=back_main, parse_mode="HTML")
    await state.update_data(msg_id=msg.message_id)

#принимаем бекап
@dp.message(backupSTATE.file, F.content_type == types.ContentType.DOCUMENT)
async def get_file_backup(message: types.Message, state: FSMContext):
    name = message.document.file_name
    if name[-6:] != 'buckup':
        return
    PATH=f'data/temp_bot/{unix_time()}_buckup.zip'
    await bot.download(message.document.file_id, PATH)
    zipf = zipfile.ZipFile(PATH, mode='r', compression=zipfile.ZIP_STORED, allowZip64=True, compresslevel=None, strict_timestamps=True, metadata_encoding=None)
    text_enter=str()
    count=int()
    for i in zipf.filelist:
        if i.filename[:8] == 'plugins/':
            zipf.extractall(path="", members=[zipf.filelist[count]])
            text_enter+=f'Был загружен плагин: {i.filename[8:]}\n'
        count+=1
    text_enter+=f'Что бы плагины вступили в силу и появились в меню надо прописать /plugin_reload\n\n'


    try:
        db.sql.close()
        zipf.extractall(path="", members=['data/DataBase.db', 'data/settings.json'])
        text_enter+=f'База заменена'
    except:
        text_enter+=f'Ошибка замены базы'
    db.sql=db.sql=db.sqlite3.connect('data//DataBase.db')
    db.cs=db.sql.cursor()
    await message.answer('<b>'+text_enter+'</b>', parse_mode="HTML")
    data=await state.update_data()
    await bot.delete_message(chat_id=cfg.admin_id, message_id=data['msg_id'])
    await message.answer(text=f'<b>🤖 Плагин: {__file__.split('/')[-1]}\n\n🏷 Название: {Main.name}\n👤 Создатель: {Main.creator}</b>', reply_markup=await admin.get_plugin_settings(Main), parse_mode="HTML")
    await state.clear()

#это мы разбрали в туториали по созданию плагинов
```

___
**Весь код**

``` python
#функция отправки бекапа
from aiogram.types.input_file import FSInputFile
from aiogram import F
from aiogram import types
from utils.plugins_biuld import BuildPlugin
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from keyb import admin
from time import time as unix_time 
from loader import dp, bot, cfg
import os
import zipfile
import shutil
from datetime import datetime
import requests
from data import db

from pip._internal.cli.main import main
try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    import apscheduler
except:
    main(["install", "apscheduler"])
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    import apscheduler

#создаем сцену для получение бекапа
class backupSTATE(StatesGroup):
    file=State()

# Определяем таймзону
TIMEZONE='Europe/Moscow'

#  scheduler для отправки сообщений в заплонированое время
scheduler=AsyncIOScheduler(timezone=TIMEZONE)

#класс для сбора бекапа
class BuildBackup():
    def __init__(self):
        self.path=f'data/temp_bot/{unix_time()}_korgi.buckup'
        self.zipf = zipfile.ZipFile(self.path, mode='w', compression=zipfile.ZIP_STORED, allowZip64=True, compresslevel=None, strict_timestamps=True, metadata_encoding=None)
        for root, dirs, files in os.walk('data/'):
            for file in files:
                if file in ['DataBase.db', 'settings.json']:
                    self.zipf.write(os.path.join(root, file))

        for root, dirs, files in os.walk('plugins/'):
            for file in files:
                if file[-2:] == 'py' and file != 'autobackup.py':
                    self.zipf.write(os.path.join(root, file))        
        self.zipf.close()

    async def close(self):
        os.remove(self.path)

#Создаем кнопку для отправки бекапа в нужный момент
inline_kb_list = [
    [InlineKeyboardButton(text="📥 Загрузить бекап", callback_data=f'upload_backup_plagin')],
    [InlineKeyboardButton(text="🗃 Бекап", callback_data=f'send_backup_plagin')]
    
    ]
#функция отправки бекапа
async def send_backup(callback):
    buckup=BuildBackup()
    document = FSInputFile(buckup.path)
    await bot.send_document(cfg.admin_id, document=document)
    await buckup.close()
    

#отправка бекапа каждыыйе 24 часа во время к нынешниму  +1 минута  времени
autobackup=scheduler.add_job(send_backup, trigger='cron', hour=datetime.now().hour, minute=datetime.now().minute+1, start_date=datetime.now(), kwargs={'callback' : types.CallbackQuery})

#функция старт для on_startup
async def start():
    scheduler.start()

Main=BuildPlugin(name='Автобэкап(встроенный)',
    creator='K1p1k',
    on_startup=start,
    keyboard=inline_kb_list
    )

#создаем хендлер
#не пугайтесь этот вы можете использовать обычный способ @dp.message
#это нужно что бы не писать вторый раз функцию send_backup
dp.callback_query.register(send_backup, F.data == 'send_backup_plagin')

#создание хендлера на обработку кнопки загрузки бекап
@dp.callback_query(F.data == 'upload_backup_plagin')
async def upload_backup_plagin(call: types.CallbackQuery, state: FSMContext):
    back_main=types.InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙", callback_data=f'plagins_settings_admin_{__file__.split('/')[-1]}')]])
    await state.set_state(state=backupSTATE.file)
    msg=await call.message.edit_text('<b>❗️ Важно: база заменяется!\n📥 Отправь backup</b>', reply_markup=back_main, parse_mode="HTML")
    await state.update_data(msg_id=msg.message_id)

#принимаем бекап
@dp.message(backupSTATE.file, F.content_type == types.ContentType.DOCUMENT)
async def get_file_backup(message: types.Message, state: FSMContext):
    name = message.document.file_name
    if name[-6:] != 'buckup':
        return
    PATH=f'data/temp_bot/{unix_time()}_buckup.zip'
    await bot.download(message.document.file_id, PATH)
    zipf = zipfile.ZipFile(PATH, mode='r', compression=zipfile.ZIP_STORED, allowZip64=True, compresslevel=None, strict_timestamps=True, metadata_encoding=None)
    text_enter=str()
    count=int()
    for i in zipf.filelist:
        if i.filename[:8] == 'plugins/':
            zipf.extractall(path="", members=[zipf.filelist[count]])
            text_enter+=f'Был загружен плагин: {i.filename[8:]}\n'
        count+=1
    text_enter+=f'Что бы плагины вступили в силу и появились в меню надо прописать /plugin_reload\n\n'


    try:
        db.sql.close()
        zipf.extractall(path="", members=['data/DataBase.db', 'data/settings.json'])
        text_enter+=f'База заменена'
    except:
        text_enter+=f'Ошибка замены базы'
    db.sql=db.sql=db.sqlite3.connect('data//DataBase.db')
    db.cs=db.sql.cursor()
    await message.answer('<b>'+text_enter+'</b>', parse_mode="HTML")
    data=await state.update_data()
    await bot.delete_message(chat_id=cfg.admin_id, message_id=data['msg_id'])
    await message.answer(text=f'<b>🤖 Плагин: {__file__.split('/')[-1]}\n\n🏷 Название: {Main.name}\n👤 Создатель: {Main.creator}</b>', reply_markup=await admin.get_plugin_settings(Main), parse_mode="HTML")
    await state.clear()

#это мы разбрали в туториали по созданию плагинов




```
