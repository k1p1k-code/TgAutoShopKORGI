from core.routers import admin_router
from loader import dp, bot
from aiogram import types, F
from keyb import admin 
from data import db
import asyncio
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import validators

class mailing_state(StatesGroup):
    message=State()
    add_btn=State()


@admin_router.callback_query(F.data == 'mailing_start')
async def milling_start(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(mailing_state.message)
    msg=await call.message.edit_text('<b>📣 Отправь сообщение которое придет всем пользователем\n🔗 Подержка: HTML(текст), ФОТО, GIF, ДОКУМЕНТОВ, ВИДЕО, АУДИО</b>', reply_markup=await admin.get_mailing(), parse_mode="HTML")
    await state.update_data(msg_id=msg.message_id, kb_list=list())

@admin_router.callback_query(mailing_state.message, F.data == 'mailing_add_button_admin')
async def add_button_mailing(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(mailing_state.add_btn)
    await call.message.edit_text(text='<b>⏹️ Отправь кнопку в таком формат:</b> <code>[текст](url)</code>\n<b>📄 Каждая кнопка с новой строки</b>', reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[admin.back_mine]]), parse_mode="HTML")


@admin_router.message(mailing_state.add_btn)
async def get_mailing_btn(message: types.Message, state: FSMContext):
    await message.delete()
    data=await state.update_data()
    data_text=message.text.split('\n')
    list_kb=data['kb_list'] 
    try:
        for i in data_text:
                i_append=list()
                for i in i.split(' '):
                    h=']('
                    i_data=i.split(h)
                    text=i_data[0][1:]
                    url=i_data[1][:-1] 
                    is_valid = validators.url(url)
                    if is_valid:
                        i_append.append(types.InlineKeyboardButton(text=text, url=url))
                list_kb.append(i_append)
    except:
        await state.set_state(mailing_state.message)
        try:
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['msg_id'], text=f'<b>❌ Ошибка добавление кнопок\n📣 Отправь сообщение которое придет всем пользователем\n🔗 Подержка: HTML(текст), ФОТО, GIF, ДОКУМЕНТОВ, ВИДЕО, АУДИО\n\n</b>', reply_markup=await admin.get_mailing(more_kb=list_kb), parse_mode="HTML")
        except:
            pass
        return
    await state.update_data(kb_list=list_kb)
    await state.set_state(mailing_state.message)
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['msg_id'], text=f'<b>📣 Отправь сообщение которое придет всем пользователем\n🔗 Подержка: HTML(текст), ФОТО, GIF, ДОКУМЕНТОВ, ВИДЕО, АУДИО\n\n</b>', reply_markup=await admin.get_mailing(more_kb=list_kb), parse_mode="HTML")

@admin_router.message(mailing_state.message, F.content_type.in_({types.ContentType.TEXT, types.ContentType.PHOTO, types.ContentType.ANIMATION, types.ContentType.DOCUMENT, types.ContentType.VIDEO, types.ContentType.AUDIO, types.ContentType.VOICE}))
async def get_milling_message(message: types.Message, state: FSMContext):
    data=await state.update_data()
    inline_kb_list=types.InlineKeyboardMarkup(inline_keyboard=data['kb_list'])
    async def TEXT_send(chat_id):
        await bot.send_message(chat_id=chat_id, text=message.text, parse_mode="HTML", reply_markup=inline_kb_list)

    async def PHOTO_send(chat_id):
        await bot.send_photo(chat_id=chat_id, photo=message.photo[-1].file_id, caption=message.caption, parse_mode="HTML", reply_markup=inline_kb_list)

    async def ANIMATION_send(chat_id):
        await bot.send_animation(chat_id=chat_id, animation=message.animation.file_id, caption=message.caption, parse_mode="HTML", reply_markup=inline_kb_list)
    
    async def DOCUMENT_send(chat_id):
        await bot.send_document(chat_id=chat_id, document=message.document.file_id, caption=message.caption, parse_mode="HTML", reply_markup=inline_kb_list)

    async def VIDEO_send(chat_id):
        await bot.send_video(chat_id=chat_id, video=message.video.file_id, caption=message.caption, parse_mode="HTML", reply_markup=inline_kb_list)

    async def AUDIO_send(chat_id):
        await bot.send_voice(chat_id=chat_id, voice=message.audio.file_id, caption=message.caption, parse_mode="HTML", reply_markup=inline_kb_list)

    async def VOICE_send(chat_id):
        await bot.send_voice(chat_id=chat_id, voice=message.voice.file_id, caption=message.caption, parse_mode="HTML", reply_markup=inline_kb_list)

    content_case={
        types.ContentType.TEXT : TEXT_send,
        types.ContentType.PHOTO : PHOTO_send,
        types.ContentType.ANIMATION : ANIMATION_send,
        types.ContentType.DOCUMENT : DOCUMENT_send,
        types.ContentType.VIDEO : VIDEO_send,
        types.ContentType.AUDIO : AUDIO_send,
        types.ContentType.VOICE : VOICE_send
    }

    for i in await db.get_allusers():
        await content_case[message.content_type](chat_id=i[0])

    #

