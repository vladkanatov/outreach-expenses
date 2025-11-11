from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from loguru import logger
from datetime import date
from database.db import add_expense
from utils.s3 import upload_file
import tempfile
import os

router = Router()

class NewExpense(StatesGroup):
    event = State()
    category = State()
    amount = State()
    description = State()
    photo = State()

@router.message(Command("new"))
async def start_new_expense(message: types.Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} начал добавление расхода")
    await message.answer("Введите название мероприятия:")
    await state.set_state(NewExpense.event)

@router.message(NewExpense.event)
async def get_event(message: types.Message, state: FSMContext):
    logger.debug(f"Получено название мероприятия: {message.text}")
    await state.update_data(event=message.text)
    await message.answer("Введите категорию расхода:")
    await state.set_state(NewExpense.category)

@router.message(NewExpense.category)
async def get_category(message: types.Message, state: FSMContext):
    logger.debug(f"Получена категория: {message.text}")
    await state.update_data(category=message.text)
    await message.answer("Введите сумму (числом):")
    await state.set_state(NewExpense.amount)

@router.message(NewExpense.amount)
async def get_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
        logger.debug(f"Получена сумма: {amount}")
    except ValueError:
        logger.warning(f"Неверный формат суммы от пользователя {message.from_user.id}: {message.text}")
        await message.answer("Введите сумму числом.")
        return
    await state.update_data(amount=amount)
    await message.answer("Введите описание:")
    await state.set_state(NewExpense.description)

@router.message(NewExpense.description)
async def get_description(message: types.Message, state: FSMContext):
    logger.debug(f"Получено описание: {message.text[:50]}...")
    await state.update_data(description=message.text)
    await message.answer("Пришлите фото (или /skip если нет):")
    await state.set_state(NewExpense.photo)

@router.message(NewExpense.photo, F.photo)
async def get_photo(message: types.Message, state: FSMContext, bot):
    logger.info(f"Получено фото от пользователя {message.from_user.id}")
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)

    # временный файл
    temp_path = tempfile.mktemp(suffix=".jpg")
    await bot.download_file(file.file_path, destination=temp_path)
    logger.debug(f"Фото сохранено во временный файл: {temp_path}")

    # загрузка в S3
    try:
        url = upload_file(temp_path)
        logger.success(f"Фото загружено в S3: {url}")
    except Exception as e:
        logger.error(f"Ошибка загрузки фото в S3: {e}")
        await message.answer("❌ Ошибка загрузки фото. Попробуйте ещё раз.")
        return
    finally:
        os.remove(temp_path)
        logger.debug("Временный файл удалён")

    await state.update_data(photo_urls=[url])
    await save_expense(message, state)

@router.message(NewExpense.photo, Command("skip"))
async def skip_photo(message: types.Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} пропустил фото")
    await state.update_data(photo_urls=[])
    await save_expense(message, state)

async def save_expense(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        await add_expense(
            user_id=message.from_user.id,
            event_name=data["event"],
            category=data["category"],
            description=data["description"],
            amount=data["amount"],
            date=date.today(),
            photo_urls=data["photo_urls"],
        )
        logger.success(
            f"Расход сохранён: user={message.from_user.id}, "
            f"event={data['event']}, amount={data['amount']}"
        )
        await message.answer("✅ Расход сохранён!")
    except Exception as e:
        logger.error(f"Ошибка сохранения расхода: {e}")
        await message.answer("❌ Ошибка сохранения. Попробуйте позже.")
    finally:
        await state.clear()