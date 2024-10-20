from aiogram.types import Message, CallbackQuery
from bot.utils import (
    check_chat_member,
    encode_referral_id,
    decode_referral_id
)
from bot.services.crud import (
    create_user,
    get_user_by_tg_id,
    get_admin_by_tg_id,
    task_reward,
    referrer_reward,
    user_statistics
)
from bot.keyboards import (
    tasks_inline_keyboard,
    start_keyboard,
    admin_start_keyboard,
    ref_link_keyboard
    )

async def start_handler(message: Message):
    username = (
        message.from_user.username
        if message.from_user.username
        else message.from_user.first_name
    )

    referral_code = None
    if len(message.text.split()) >= 2:
        referral_code = message.text.split()[1]
        try:
            referral_code = decode_referral_id(referral_code)
        except ValueError:
            referral_code = None

    user = await get_user_by_tg_id(tg_id=message.from_user.id)
    
    if not user:
        user = await create_user(
            tg_id=message.from_user.id,
            username=username,
            referrer=referral_code
        )
    admin = await get_admin_by_tg_id(tg_id=message.from_user.id)
    if admin:
        keyboard = admin_start_keyboard()
    else:
        keyboard = start_keyboard()    
    await message.answer("👋 Hello! Complete tasks, invite friends, and earn rewards!", reply_markup=keyboard)

async def tasks_handler(message: Message):
    user = await get_user_by_tg_id(tg_id=message.from_user.id)
    if user.complete_tasks:
        return await message.answer("All tasks is completed")
    inline_kb = tasks_inline_keyboard()
    return await message.answer("Complete tasks to get rewards:", reply_markup=inline_kb)
    


async def ref_link_handler(message: Message):
    user = await get_user_by_tg_id(tg_id=message.from_user.id)

    if not user.complete_tasks:
        return await message.answer("💡 You need to complete tasks first to get your referral link.")
    
    hash_id = encode_referral_id(message.from_user.id)
    link = f"https://t.me/adtgtestbot?start={hash_id}"
    keyboard = ref_link_keyboard(hash_id=hash_id)
    return await message.answer(f"🔗 Your referral link: {link}", reply_markup=keyboard)


async def stats_handler(message: Message):
    user = await get_user_by_tg_id(tg_id=message.from_user.id)
    points = str(user.points)
    await message.answer(f"🏆 You have {points} points!")


async def callback_check_btn(callback_query: CallbackQuery):
    user = await get_user_by_tg_id(tg_id=callback_query.from_user.id)
    if user.complete_tasks:
        return await callback_query.message.answer("✅ You have completed all tasks!")
    
    member_status = await check_chat_member(
        chat_id="-1002301909788",
        telegram_id=callback_query.from_user.id,
        bot=callback_query.bot
    )
    
    if member_status:
        await task_reward(tg_id=callback_query.from_user.id)
        if user.referrer:
            referrer_id = user.referrer
            ref_reward = 15 if callback_query.from_user.is_premium else 5
            await referrer_reward(referrer_id=referrer_id, reward=ref_reward)
        return await callback_query.message.answer("🎉 Tasks completed! You received a reward.")
    
    return await callback_query.message.answer("❌ Tasks are not completed yet. Subscribe to the channel and try again.")

async def bot_stats(message: Message):
    if await get_admin_by_tg_id(message.from_user.id):
        statistic = await user_statistics()
        msg = (
            f"Total users: {statistic['total_users']}\n"
            f"Complete task users: {statistic['complete_task_users']}\n"
            f"Not complete task users: {statistic['not_complete_tasks_users']}"
        )
        return await message.answer(msg)
    
    return await message.answer("Вы не являетесь администратором.")