import asyncpg
from loguru import logger
from config import DATABASE_URL

async def init_db():
    """Проверка подключения к БД. Миграции выполняются через yoyo."""
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.close()
        logger.success("Подключение к базе данных успешно")
    except Exception as e:
        logger.error(f"Не удалось подключиться к БД: {e}")
        raise

async def get_connection():
    return await asyncpg.connect(DATABASE_URL)

async def add_expense(user_id: int, event_name: str, category: str,
                      amount: float, date, photo_urls: list[str]):
    conn = await get_connection()
    await conn.execute("""
        INSERT INTO expenses (user_id, event_name, category, amount, date, photo_urls)
        VALUES ($1, $2, $3, $4, $5, $6)
    """, user_id, event_name, category, amount, date, photo_urls)
    await conn.close()

async def list_expenses(limit: int = 5):
    conn = await get_connection()
    try:
        rows = await conn.fetch("""
            SELECT event_name, amount, category, date FROM expenses
            ORDER BY id DESC
            LIMIT $1
        """, limit)
        logger.debug(f"Получено {len(rows)} расходов из БД")
        return rows
    except Exception as e:
        logger.error(f"Ошибка при получении списка расходов: {e}")
        raise
    finally:
        await conn.close()
