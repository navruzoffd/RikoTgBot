from aiogram import Bot
from aiogram.types import BotCommandScopeChat, Message, CallbackQuery, WebAppInfo
from aiogram.types.menu_button_web_app import MenuButtonWebApp
from aiogram.exceptions import TelegramBadRequest
import base64
from bot.core.config import settings

def encode_referral_id(user_id: int) -> str:
    return base64.urlsafe_b64encode(str(user_id).encode()).decode()

def decode_referral_id(encoded_id: str) -> int:
    return int(base64.urlsafe_b64decode(encoded_id.encode()).decode())

async def set_menu_button(mes: Message | CallbackQuery, locale: str = None) -> None:
    await mes.bot.set_chat_menu_button(
        chat_id=mes.from_user.id,
        menu_button=MenuButtonWebApp(text=_("Play", locale=locale), web_app=WebAppInfo(url=settings.MINI_APP_URL)),
    )

    await mes.bot.delete_my_commands(
        scope=BotCommandScopeChat(chat_id=mes.from_user.id),
    )



async def check_chat_member(chat_id: str, telegram_id: int, bot: Bot) -> bool:
    try:
        chat_member = await bot.get_chat_member(chat_id=chat_id, user_id=telegram_id)
        return chat_member.status in {"member", "administrator", "creator"}
    except TelegramBadRequest as e:
        if "chat not found" in e.message:
            return False
        elif "PARTICIPANT_ID_INVALID" in e.message:
            return False