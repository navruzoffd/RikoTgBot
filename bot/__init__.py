import asyncio

from random import randint

from aiogram import Bot, Dispatcher
from bot.constants import Mesages
from bot.core.logger import logger
from bot.handler import register_handlers

from config import settings

async def setup_bot_settings(bot: Bot, dp: Dispatcher) -> None:
    await asyncio.sleep(randint(1, 30))
    webhook_info = await bot.get_webhook_info()

    logger.info(f"Webhook info: {webhook_info.url}")

    if f"{settings.WEBHOOK_URL}{settings.WEBHOOK_PATH}" != webhook_info.url:
        logger.info(f"Setup webhook url: {settings.WEBHOOK_URL}{settings.WEBHOOK_PATH}")
        try:
            await bot.set_webhook(
                f"{settings.WEBHOOK_URL}{settings.WEBHOOK_PATH}",
                max_connections=100000,
                secret_token=settings.SECRET_TOKEN,
                allowed_updates=["message", "callback_query"],
            )
        except Exception as e:
            logger.warning(f"Failed to setup webhook: {e}")

    await bot.set_my_description(description=Mesages.DESCRIPTION)
    await bot.set_my_short_description(short_description=Mesages.SHORT_DESCRIPTION)

    register_handlers(dp)

    logger.info("Webhook worker started")