from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from loader import cfg, dp
import utils
from typing import Callable, Dict, Any, Awaitable
import json
from data import db
from aiogram import types

class OnlyPrivate(BaseMiddleware):
    async def __call__(
        self,
        handlers: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]) -> Any:
        try:
            if event.chat.type != 'private':
                return
        except:
            if event.message.chat.type != 'private':
                return

class BunUsers(BaseMiddleware):
    async def __call__(
        self,
        handlers: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]) -> Any:
        try:
            if not (await db.get_banUser(user_id=event.from_user.id))[0]:
                return
        except:
            pass
        return await handlers(event, data)

class IsWork(BaseMiddleware):
    async def __call__(
        self,
        handlers: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]) -> Any:
        PATH='data/settings.json'
        data_json=json.load((open(PATH, 'r', encoding='UTF-8')))
        if data_json['work'] == False and event.from_user.id != cfg.admin_id:
            return
        return await handlers(event, data)
    
dp.message.middleware(OnlyPrivate())
dp.callback_query.middleware(OnlyPrivate())


dp.message.middleware(BunUsers())
dp.callback_query.middleware(BunUsers())

dp.message.middleware(IsWork())
dp.callback_query.middleware(IsWork())