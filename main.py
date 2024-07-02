import os
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

#Підтягуємо хендлери
from app.handlers import router

# Завантаження змінних середовища з файлу .env
load_dotenv()

# Отримання значень змінних середовища
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Ініціалізація бота і диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    # Тіло бота
    dp.include_router(router)
    await bot.delete_webhook(True, 1)
    await dp.start_polling(bot)  

# Запуск бота
if __name__ == '__main__':
    print("Start polling...")
    asyncio.run(main())
