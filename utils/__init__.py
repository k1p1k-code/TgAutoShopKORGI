from loader import bot, dp, cache
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
import json




async def clear_state(user_id, chat_id):
    user_id = user_id 
    chat_id = chat_id 

    state_with: FSMContext = FSMContext(
        storage=dp.storage, 
        key=StorageKey(
            chat_id=chat_id,
            user_id=user_id,  
            bot_id=bot.id))
    await state_with.clear()

async def check_spam(user_id):
    
    if user_id == cache.get(user_id):
        return True
    cache[user_id]=user_id
    return False
        


