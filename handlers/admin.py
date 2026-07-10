import os
from aiogram import Router, F
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.filters import Command

from config import ADMIN_ID
from database.db import get_new_requests, close_request
from keyboards.inline import get_admin_request_kb

router = Router()

@router.message(Command("admin"))
async def view_requests(message: Message):
    if str(message.from_user.id) != str(ADMIN_ID):
        await message.answer("⛔ У вас нет прав.")
        return

    requests = await get_new_requests()

    if not requests:
        await message.answer("🎉 Новых заявок пока нет!")
        return

    await message.answer(f"📋 Найдено новых заявок: {len(requests)}")

    for req in requests:
        text = (
            f"🚨 <b>Заявка #{req['id']}</b>\n"
            f"📍 <b>Район:</b> {req['district']}\n"
            f"🛠 <b>Категория:</b> {req['category']}\n"
            f"📝 <b>Описание:</b> {req['description']}\n"
            f"📞 <b>Контакты:</b> {req['contacts']}"
        )
        
        # --- ИСПРАВЛЕНИЕ ЗДЕСЬ ---
        # Мы точно знаем, что картинка всегда называется "photos/{номер_заявки}.jpg"
        expected_photo_path = f"photos/{req['id']}.jpg"
        
        keyboard = get_admin_request_kb(req['id'])

        # Проверяем, существует ли физически такой файл
        if os.path.exists(expected_photo_path):
            photo = FSInputFile(expected_photo_path)
            # Отправляем ФОТОГРАФИЮ, а текст делаем подписью к ней (caption)
            await message.answer_photo(photo=photo, caption=text, parse_mode="HTML", reply_markup=keyboard)
        else:
            # Если файла нет (пользователь нажал "Пропустить"), отправляем только текст
            await message.answer(text, parse_mode="HTML", reply_markup=keyboard)

@router.callback_query(F.data.startswith("close_"))
async def process_close_request(callback: CallbackQuery):
    req_id = int(callback.data.split("_")[1])
    await close_request(req_id)
    
    status_text = "\n\n<b>✅ ЗАЯВКА ЗАКРЫТА</b>"
    
    try:
        new_text = callback.message.caption + status_text
        await callback.message.edit_caption(caption=new_text, parse_mode="HTML", reply_markup=None)
    except:
        new_text = callback.message.text + status_text
        await callback.message.edit_text(text=new_text, parse_mode="HTML", reply_markup=None)

    await callback.answer(f"Заявка #{req_id} успешно закрыта!", show_alert=True)