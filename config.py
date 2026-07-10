import os
from dotenv import load_dotenv

load_dotenv() # Загружаем секреты из .env

TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')

# Районы работы (можно легко добавлять новые)
DISTRICTS = ["ЦАО", "ЗАО", "ЮАО", "ВАО", "САО"]

# Сценарии (Категории заявок)
CATEGORIES = ["Настройка связи", "Установка приложений", "Вопросы безопасности"]