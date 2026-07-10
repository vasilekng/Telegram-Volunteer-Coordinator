import asyncio
import logging
import sys
import os 
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession 

from handlers import user_request, admin

from config import TOKEN
from database.db import db_start


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("requests_log.txt", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

async def main():
    await db_start()

    # Проверяем, запущен ли код на сервере PythonAnywhere
    if "PYTHONANYWHERE_DOMAIN" in os.environ:
        # Если да, используем их обязательный прокси
        session = AiohttpSession(proxy="http://proxy.server:3128")
        bot = Bot(token=TOKEN, session=session)
        logging.info("Подключение через прокси PythonAnywhere...")
    else:
        # Если код запущен на вашем домашнем ПК, работаем как обычно
        bot = Bot(token=TOKEN)
    # =================================

    dp = Dispatcher()
    dp.include_router(user_request.router)
    dp.include_router(admin.router)
    logging.info("Бот успешно запущен и ожидает сообщения!")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен.")