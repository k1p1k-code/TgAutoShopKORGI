from aiogram.types.input_file import FSInputFile
from aiogram import F
from aiogram import types
from utils.plugins_biuld import BuildPlugin
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from keyb import admin
from time import time as unix_time 
from loader import dp, bot, cfg, scheduler
import os
import zipfile
from datetime import datetime
from data import db

#создаем сцену для получение бекапа
class backupSTATE(StatesGroup):
    file=State()

# Определяем таймзону


#  scheduler для отправки сообщений в заплонированое время


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
#scheduler.add_job(send_backup, trigger='cron', hour=datetime.now().hour, minute=datetime.now().minute+1, start_date=datetime.now(), kwargs={'callback' : types.CallbackQuery})

#функция старт для on_startup
async def start():
    pass

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
    text_enter+=f'Что бы плагины вступили в силу и появились в меню надо перезапустить бота\n\n'


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

