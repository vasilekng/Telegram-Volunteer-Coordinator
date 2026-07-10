from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from config import CATEGORIES, DISTRICTS

def get_categories_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for cat in CATEGORIES:
        builder.add(KeyboardButton(text=cat))
    builder.adjust(2) 
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_districts_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for dist in DISTRICTS:
        builder.add(KeyboardButton(text=dist))
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_skip_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Пропустить")]], 
        resize_keyboard=True, 
        one_time_keyboard=True
    )