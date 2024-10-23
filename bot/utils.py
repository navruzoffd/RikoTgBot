from aiogram import Bot
from aiogram.types import BotCommandScopeChat, Message, CallbackQuery, WebAppInfo
from aiogram.types.menu_button_web_app import MenuButtonWebApp
from aiogram.exceptions import TelegramBadRequest
import base64
import urllib.parse
from bot.core.config import settings

def encode_referral_id(user_id: int) -> str:
    return base64.urlsafe_b64encode(str(user_id).encode()).decode()

def decode_referral_id(encoded_id: str) -> int:
    return int(base64.urlsafe_b64decode(encoded_id.encode()).decode())

def gen_x_link(hash_id):
    text = f"Check out $RIKO, the fearless pet of GRA.FUN! Join the community and earn points with my referral link! 👇 \nhttps://t.me/adtgtestbot?start={hash_id}\nBSC is ours for the taking! 🏴‍☠️"
    encoded_text = urllib.parse.quote(text, safe='')
    link = "https://twitter.com/intent/tweet?text="+encoded_text
    return link

def start_msg():
    msg = (
        "Hi! Welcome to the RIKO referral program! 👥\n\n"
        "RIKO is a meme coin symbolized by the fearless honey badger, dedicated to "
        "building a strong, engaged community in the cryptocurrency space. "
        "Launched on the Gra.fun platform, RIKO emphasizes accessibility and "
        "community involvement at its core.\n\n"
        "Complete a few simple steps to unlock your referral link and start earning "
        "points for inviting friends. 🧡"
    )
    return msg

def tasks_msg():
    msg = (
        "Complete these tasks to unlock your referral link:\n\n"
        "1️⃣ Follow RIKO on Twitter — 25 points\n"
        "2️⃣ Subscribe to RIKO on Telegram — 25 points\n\n"
        "Once done, press 'Check'. Good luck! 🌟"
    )
    return msg

def complete_tasks_msg():
    msg = (
        "Great job! You've earned 50 points for completing all tasks! 🎉\n\n"
        "Now you have access to your referral link.\n\n"
        "Share it with friends and earn points for each referral: 5 points for regular users and 15 points for premium users. 👥"
    )
    return msg


async def check_chat_member(chat_id: str, telegram_id: int, bot: Bot) -> bool:
    try:
        chat_member = await bot.get_chat_member(chat_id=chat_id, user_id=telegram_id)
        return chat_member.status in {"member", "administrator", "creator"}
    except TelegramBadRequest as e:
        if "chat not found" in e.message:
            return False
        elif "PARTICIPANT_ID_INVALID" in e.message:
            return False