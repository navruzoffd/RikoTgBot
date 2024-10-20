from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup
)

def tasks_inline_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Telegram", url="https://t.me/testchatteuirkdk")],
        [InlineKeyboardButton(text="🐦 Follow Elon Musk on X", url="https://x.com/elonmusk")],
        [InlineKeyboardButton(text="✅ Check Tasks", callback_data="check_btn")]
    ])
    return keyboard

def ref_link_keyboard(hash_id: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📤 Share Your Referral Link", url=f"https://t.me/share/url?url=https://t.me/adtgtestbot?start={hash_id}&text=Some Text")]
    ])
    return keyboard

def start_keyboard():
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📝 Tasks"), KeyboardButton(text="📊 My Stats")],
        [KeyboardButton(text="👥 Invite Friends")],
    ], resize_keyboard=True)
    return keyboard


def admin_start_keyboard():
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📝 Tasks"), KeyboardButton(text="📊 My Stats")],
        [KeyboardButton(text="👥 Invite Friends")],
        [KeyboardButton(text="🤖 Bot Stats")],
    ], resize_keyboard=True)
    return keyboard
