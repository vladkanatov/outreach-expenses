from aiogram import Bot
from loguru import logger
from datetime import date
from config import BOT_TOKEN, NOTIFICATION_CHAT_ID

async def send_expense_notification(
    user_id: int,
    username: str,
    event_name: str,
    category: str,
    amount: float,
    expense_date: date,
    has_photo: bool = False
):
    """
    Отправляет уведомление о новом чеке в указанный чат
    
    Args:
        user_id: Telegram ID пользователя, добавившего расход
        username: Имя пользователя
        event_name: Название мероприятия
        category: Категория расхода
        amount: Сумма расхода
        expense_date: Дата расхода
        has_photo: Есть ли приложенное фото
    """
    try:
        bot = Bot(token=BOT_TOKEN)
        
        # Формируем сообщение
        message_text = (
            "🧾 <b>Новый чек добавлен</b>\n\n"
            f"👤 Пользователь: {username} (ID: {user_id})\n"
            f"🎯 Мероприятие: <b>{event_name}</b>\n"
            f"📂 Категория: {category}\n"
            f"💰 Сумма: <b>{amount:.2f} ₽</b>\n"
            f"📅 Дата: {expense_date.strftime('%d.%m.%Y')}\n"
            f"📸 Фото: {'✅ Да' if has_photo else '❌ Нет'}"
        )
        
        await bot.send_message(
            chat_id=NOTIFICATION_CHAT_ID,
            text=message_text,
            parse_mode="HTML"
        )
        
        logger.success(f"Уведомление о расходе отправлено в чат {NOTIFICATION_CHAT_ID}")
        
        await bot.session.close()
        
    except Exception as e:
        logger.error(f"Ошибка отправки уведомления: {e}")
        # Не прерываем выполнение, если уведомление не отправилось
