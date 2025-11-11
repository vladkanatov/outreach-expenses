import asyncio
from aiogram import Bot, Dispatcher
from loguru import logger
from config import BOT_TOKEN
from database.db import init_db
from handlers import start, new_expense

# Настройка логирования
logger.add(
    "logs/bot.log",
    rotation="10 MB",
    retention="7 days",
    compression="zip",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
)

async def main():
    logger.info("Запуск бота...")
    
    try:
        await init_db()
        logger.success("Подключение к базе данных установлено")
    except Exception as e:
        logger.error(f"Ошибка подключения к БД: {e}")
        raise

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(new_expense.router)
    logger.info("Роутеры подключены")

    logger.success("🤖 Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.exception(f"Критическая ошибка: {e}")
