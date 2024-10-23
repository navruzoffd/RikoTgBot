from aiogram import Router, F
from aiogram.filters import CommandStart, Command

from bot.handler.handlers import (
    start_handler,
    ref_link_handler,
    stats_handler,
    callback_check_btn,
    bot_stats,
    tasks_handler,
    friends_stats_handler,
    go_to_stats_menu,
    back_to_menu
)


def register_handlers(router: Router) -> None:
    router.message.register(start_handler, CommandStart())
    router.message.register(ref_link_handler, F.text == "👥 Invite Friends")
    router.message.register(stats_handler, F.text == "📈 My Stats")
    router.message.register(bot_stats, F.text == "🤖 Bot Stats")
    router.message.register(tasks_handler, F.text == "📝 Tasks")
    router.message.register(go_to_stats_menu, F.text == "📊 Stats")
    router.message.register(friends_stats_handler, F.text == "📊 Friends Stats")
    router.message.register(back_to_menu, F.text == "🔙 Back")
    router.callback_query.register(callback_check_btn, lambda c: c.data == "check_btn")