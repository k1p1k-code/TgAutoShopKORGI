from aiogram import Router, F, types
from loader import dp, cfg
admin_router=Router()
admin_router.message.filter(F.chat.id == cfg.admin_id)
admin_router.callback_query.filter(F.message.chat.id == cfg.admin_id)
dp.include_router(admin_router)