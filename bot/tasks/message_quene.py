from asyncio import Queue
import asyncio

from aiogram.exceptions import TelegramRetryAfter
from aiogram import Bot, Dispatcher

from bot.core.logger import logger


class MessageQuene:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.dp = dp
        self.bot = bot
        self._quene = Queue(maxsize=1000000)

    async def add_message(self, message):
        await self._quene.put(message)

    async def start(self): 
        while True:
            try:
                message = await self._quene.get()
                await self.send_message(message)
            except Exception as e:
                logger.exception(f"Failed to process update {e}")

    async def send_message(self, message):
        try:
            await self.dp.feed_update(bot=self.bot, update=message)
        except TelegramRetryAfter as e:
            logger.warning(f"Retry after {e.retry_after} seconds")
            await asyncio.sleep(e.retry_after + 1)
            await self.dp.feed_update(bot=self.bot, update=message)
        except Exception as e:
            logger.exception(f"Failed to process update {e}")
        
        await asyncio.sleep(0.035)

