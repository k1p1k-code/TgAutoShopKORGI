from progress.bar import IncrementalBar
bar = IncrementalBar('Loading...', max=5)
from aiogram import Bot, Dispatcher

import config as cfg
bar.next()
from aiogram.fsm.storage.memory import MemoryStorage
bar.next()
from apscheduler.schedulers.asyncio import AsyncIOScheduler
bar.next()
import os
from cachetools import TTLCache
bar.next()
bar.finish()
import json
import shutil

if 'custom_cfg.json' in os.listdir('data//temp_bot'):
    data=json.load((open('data//temp_bot//custom_cfg.json', 'r', encoding='UTF-8')))
    if data.get('token_bot') != None:
        cfg.token_bot=data.get('token_bot')

    if data.get('admin_id') != None:
        cfg.admin_id=data.get('admin_id')

    if data.get('timezone') != None:
        cfg.timezone=data.get('timezone')
os.remove("data//temp_bot//custom_cfg.json")

bot=Bot(cfg.token_bot)
dp=Dispatcher(bot=bot, storage=MemoryStorage())


scheduler=AsyncIOScheduler(timezone=cfg.timezone)
cache=TTLCache(maxsize=10100, ttl=4)
bar.next()