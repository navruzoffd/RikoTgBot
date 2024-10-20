from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database import SessionLocal, User, Admin
from bot.core.logger import logger


async def create_user(tg_id: int, username: str, referrer: int) -> User:
    async with SessionLocal() as session:
        new_user = User(tg_id=tg_id, username=username, referrer=referrer)
        session.add(new_user)
        await session.commit()
        return new_user


async def get_user_by_tg_id(tg_id: int, session: AsyncSession | None = None) -> User | None:
    try:
        if session is None:
            async with SessionLocal() as session:
                result = await session.execute(select(User).where(User.tg_id == tg_id))
                return result.scalars().first()
        else:
            result = await session.execute(select(User).where(User.tg_id == tg_id))
            return result.scalars().first()
    except Exception as e:
        logger.exception(f"Database error | {e}")

from sqlalchemy import update

async def task_reward(tg_id: int):
    async with SessionLocal() as session:
        query = (
            update(User)
            .where(User.tg_id == tg_id)
            .values(complete_tasks=True, points=User.points + 50)
        )
        await session.execute(query)
        await session.commit()

async def referrer_reward(referrer_id: int, reward :int):
    async with SessionLocal() as session:
        query = (
            update(User)
            .where(User.tg_id == referrer_id)
            .values(points=User.points + reward)
        )
        await session.execute(query)
        await session.commit()

async def get_admin_by_tg_id(tg_id: int) -> Admin | None:
    try:
        async with SessionLocal() as session:
            admin = await session.execute(
                select(Admin).join(User).filter(User.tg_id == tg_id)
            )
            return admin.scalars().first()
    except Exception as e:
        logger.exception(f"Database error | {e}")

async def user_statistics() -> dict:
    async with SessionLocal() as session:
        total_users = await session.execute(select(func.count(User.id)))
        complete_task_users = await session.execute(select(func.count(User.id)).where(User.complete_tasks.is_(True)))
        not_complete_tasks_users = await session.execute(select(func.count(User.id)).where(User.complete_tasks.is_(False)))

        return {
            "total_users": total_users.scalar(),
            "complete_task_users": complete_task_users.scalar(),
            "not_complete_tasks_users": not_complete_tasks_users.scalar()
        }

    

async def change_user_language(tg_id: int, language_code: str) -> User | None:
    async with SessionLocal() as session:
        if not (exist_user := await get_user_by_tg_id(tg_id=tg_id, session=session)):
            return None
        exist_user.language_code = language_code
        session.add(exist_user)
        await session.commit()
        await session.refresh(exist_user)
        return exist_user


async def get_user_language(tg_id: int) -> str:
    user = await get_user_by_tg_id(tg_id=tg_id)

    if not user:
        return "en"
    
    return user.language_code
