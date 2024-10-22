from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup
)

from bot.utils import gen_x_link

def tasks_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Telegram", url="https://t.me/testchatteuirkdk")],
        [InlineKeyboardButton(text="🐦 Follow on X", url="https://x.com/elonmusk")],
        [InlineKeyboardButton(text="✅ Check", callback_data="check_btn")]
    ])
    return keyboard

def ref_link_keyboard(hash_id: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✈️ Share on Telegram", url=f"https://t.me/share/url?url=https://t.me/adtgtestbot?start={hash_id}&text=Some Text")],
        [InlineKeyboardButton(text="🐦 Share on Twitter", url=f"{gen_x_link(hash_id)}")]
    ])
    return keyboard

def start_keyboard():
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📝 Tasks"), KeyboardButton(text="📊 My Stats")],
        [KeyboardButton(text="👥 Invite Friends"), KeyboardButton(text="📊 Friends Stats")]
    ], resize_keyboard=True)
    return keyboard


def admin_start_keyboard():
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📝 Tasks"), KeyboardButton(text="📊 My Stats")],
        [KeyboardButton(text="👥 Invite Friends")],
        [KeyboardButton(text="🤖 Bot Stats")],
    ], resize_keyboard=True)
    return keyboard
