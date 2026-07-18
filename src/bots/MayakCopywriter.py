import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.session.aiohttp import AiohttpSession

from src.rag.chain import get_mayakovsky_response_copywriter

load_dotenv()

# ==================== ЛОГИРОВАНИЕ ====================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ==================== КОНФИГУРАЦИЯ ====================
TOKEN = os.getenv("MAYAKCOPYWRITER_TOKEN")
if not TOKEN:
    raise ValueError("Токен Telegram не найден! Проверь файл .env")

# PROXY_URL = "http://127.0.0.1:12334"

dp = Dispatcher()

# ==================== ОБРАБОТЧИКИ ====================
@dp.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = (
        "Я — Владимир Маяковский, главный рекламщик «Окон РОСТА»!\n\n"
        "Нужна реклама, бьющая точно в цель? Напиши мне, что ты продаешь (продукт, идею, услугу).\n"
        "Я выдам тебе такой слоган, что конкуренты разбегутся в страхе!"
    )
    await message.answer(welcome_text)


@dp.message(F.text)
async def handle_user_complaint(message: Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action='typing')

    try:
        bot_answer = get_mayakovsky_response_copywriter(message.text)
        await message.answer(bot_answer)
    except Exception as e:
        logger.error(f"Ошибка при генерации ответа: {e}")
        await message.answer("Сбой на линии! Мои футуристические шестеренки заклинило. Попробуй еще раз, товарищ.")


# ==================== ЗАПУСК ====================
async def main():
    # session = AiohttpSession(proxy=PROXY_URL)

    bot = Bot(token=TOKEN)#, session=session)

    logger.info("Товарищ Маяковский вышел на линию. Бот запущен!")

    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())