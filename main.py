import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException

from aiogram import types
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties

from config import settings
from bot.core.logger import logger

from bot import setup_bot_settings
from bot.tasks.message_quene import MessageQuene


dp = Dispatcher()
bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode="Markdown"))
message_queue = MessageQuene(bot, dp)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(message_queue.start())
    await setup_bot_settings(bot, dp)

    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

    await bot.delete_webhook()


app = FastAPI(
    lifespan=lifespan,
    # openapi_url=None,
    # # docs_url=None,
    # redoc_url=None,
)


@app.post(settings.WEBHOOK_PATH)
async def bot_webhook(request: Request):
    secret_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if secret_token != settings.SECRET_TOKEN:
        logger.error("Wrong secret token")
        raise HTTPException(status_code=403, detail="Forbidden")

    update = await request.json()
    telegram_update = types.Update(**update)

    try:
        await message_queue.add_message(telegram_update)
    except Exception as e:
        logger.exception(f"Failed to process update {e}")
    return
