from aiogram import Router, types
from aiogram.filters import Command
from loguru import logger

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    logger.info(f"Команда /start от пользователя {message.from_user.id} (@{message.from_user.username})")
    await message.answer(
        "👋 Привет! Я бот для учёта расходов.\n\n"
        "Команды:\n"
        "/new - добавить новый расход\n"
        "/start - показать это сообщение"
    )
