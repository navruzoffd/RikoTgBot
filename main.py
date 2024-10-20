import asyncio
from bot.handler import register_handlers
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config import settings
from bot.tasks.message_quene import MessageQuene


bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode="Markdown"))
dp = Dispatcher()
message_queue = MessageQuene(bot, dp)

async def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    register_handlers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
