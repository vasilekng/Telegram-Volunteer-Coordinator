import os
from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.reply import get_categories_kb, get_districts_kb, get_skip_kb
from database.db import create_request

router = Router()

# Шаги создания заявки
class RequestForm(StatesGroup):
    choosing_category = State()
    choosing_district = State()
    writing_description = State()
    writing_contacts = State()
    sending_photo = State()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        "👋 Добро пожаловать в волонтерский центр!\nВыберите категорию помощи:",
        reply_markup=get_categories_kb()
    )
    await state.set_state(RequestForm.choosing_category)

@router.message(RequestForm.choosing_category)
async def process_category(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer("📍 В каком районе вы находитесь?", reply_markup=get_districts_kb())
    await state.set_state(RequestForm.choosing_district)

@router.message(RequestForm.choosing_district)
async def process_district(message: Message, state: FSMContext):
    await state.update_data(district=message.text)
    await message.answer(
        "📝 Опишите вашу проблему подробно (Текстом):", 
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(RequestForm.writing_description)

@router.message(RequestForm.writing_description)
async def process_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("📞 Оставьте ваши контакты (телефон или никнейм):")
    await state.set_state(RequestForm.writing_contacts)

@router.message(RequestForm.writing_contacts)
async def process_contacts(message: Message, state: FSMContext):
    await state.update_data(contacts=message.text)
    await message.answer(
        "📸 Прикрепите фото проблемы (или нажмите кнопку 'Пропустить'):",
        reply_markup=get_skip_kb()
    )
    await state.set_state(RequestForm.sending_photo)

@router.message(RequestForm.sending_photo)
async def process_photo(message: Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    photo_path = "Нет фото"

    # Если пользователь прислал фото
    if message.photo:
        file = await bot.get_file(message.photo[-1].file_id)
        temp_path = f"photos/temp_{message.from_user.id}.jpg"
        await bot.download_file(file.file_path, temp_path)
        photo_path = temp_path
        
    # Если написал текст, но это не кнопка "Пропустить"
    elif message.text and message.text.lower() != "пропустить":
        await message.answer("Пожалуйста, прикрепите фотографию или нажмите кнопку 'Пропустить'.")
        return # Прерываем функцию, ждем дальше

    # Сохраняем в БД
    req_id = await create_request(
        user_id=message.from_user.id,
        category=user_data['category'],
        district=user_data['district'],
        desc=user_data['description'],
        contacts=user_data['contacts'],
        photo=photo_path
    )

    # Переименовываем фото в "номер_заявки.jpg"
    if message.photo:
        final_path = f"photos/{req_id}.jpg"
        os.rename(temp_path, final_path)

    await message.answer(
        f"✅ Заявка №{req_id} успешно создана!\nВолонтеры скоро свяжутся с вами.",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()