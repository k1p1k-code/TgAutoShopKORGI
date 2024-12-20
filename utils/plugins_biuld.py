from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from loader import dp, bot

class BuildPlugin():
    def __init__(self, name, creator, on_startup=str, keyboard=list()):
        self.name=name
        self.creator=creator
        self.on_startup=on_startup
        self.keyboard=keyboard


    class state():
        async def set(state, chat_id, user_id):
            user_id = user_id # юзер айди искомого юзера
            chat_id = chat_id # чат айди, где находится юзер

            state_with: FSMContext = FSMContext(
                storage=dp.storage, # dp - экземпляр диспатчера 
                key=StorageKey(
                    chat_id=chat_id, # если юзер в ЛС, то chat_id=user_id
                    user_id=user_id,  
                    bot_id=bot.id))
            await state_with.set_state(state)
        
        async def clear(chat_id, user_id):
            user_id = user_id # юзер айди искомого юзера
            chat_id = chat_id # чат айди, где находится юзер

            state_with: FSMContext = FSMContext(
                storage=dp.storage, # dp - экземпляр диспатчера 
                key=StorageKey(
                    chat_id=chat_id, # если юзер в ЛС, то chat_id=user_id
                    user_id=user_id,  
                    bot_id=bot.id))
            await state_with.clear()