from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from database.model import User, QuizResult
from datetime import datetime, timedelta


async def orm_add_bot_users(session: AsyncSession, user_id, name, username):
    obj = User(
        telegram_id=user_id,
        name=name,
        username=username,
        is_admin=False,
    )
    session.add(obj)
    await session.commit()


async def orm_add_admin(session: AsyncSession, user_id, name, username):
    # Проверяем, существует ли уже администратор с таким telegram_id
    result = await session.execute(select(User).filter_by(telegram_id=user_id))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        # Если пользователь уже существует, обновляем его данные
        existing_user.name = name
        existing_user.username = username
        existing_user.is_admin = True
        await session.commit()
        return existing_user
    else:
        # Если пользователь не существует, создаем нового
        new_user = User(
            telegram_id=user_id,
            name=name,
            username=username,
            is_admin=True
        )
        session.add(new_user)
        await session.commit()
        return new_user


async def orm_get_id_bot_user(session: AsyncSession):
    query = select(User.telegram_id)
    result = await session.execute(query)
    return result.scalars().all()


async def get_admins(session: AsyncSession):
    query = select(User.telegram_id).filter(User.is_admin == True)
    result = await session.execute(query)
    return result.scalars().all()


async def get_admin(session: AsyncSession):
    query = select(User).filter(User.is_admin == True)  # Фильтруем только администраторов
    result = await session.execute(query)
    return result.scalars().all()


async def get_admin_by_id(session: AsyncSession, user_id: int):
    query = select(User).filter(User.user_id == user_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def remove_admin(session: AsyncSession, user_id: int):
    # Выполняем запрос на удаление администратора по user_id
    query = select(User).filter(User.user_id == user_id)
    result = await session.execute(query)
    admin = result.scalar_one_or_none()

    if admin:
        # Удаляем администратора
        await session.delete(admin)
        await session.commit()


async def get_total_users(session: AsyncSession) -> int:
    result = await session.execute(select(User))
    return len(result.scalars().all())


async def get_total_admins(session: AsyncSession) -> int:
    result = await session.execute(select(User).filter(User.is_admin == True))
    return len(result.scalars().all())


async def get_user_creation_dates(session: AsyncSession):
    earliest = await session.execute(select(func.min(User.created)))
    latest = await session.execute(select(func.max(User.created)))

    return {
        "earliest": earliest.scalar(),
        "latest": latest.scalar()
    }


async def get_users_created_last_days(session: AsyncSession, days: int) -> int:
    start_date = datetime.now() - timedelta(days=days)
    query = select(User).filter(User.created >= start_date)
    result = await session.execute(query)
    return len(result.scalars().all())


async def save_quiz_result(user_id: int, correct_answers: int, total_questions: int, session: Session):
    result = QuizResult(
        user_id=user_id,
        score=correct_answers,
        total_questions=total_questions,
    )

    session.add(result)
    await session.commit()

    print(f"Результат викторины для пользователя {user_id} успешно сохранен!")

    return result


def calculate_and_save_quiz_result(session: Session, user_id: int, correct_answers: int, total_questions: int):
    result = QuizResult(
        user_id=user_id,
        score=correct_answers,
        total_questions=total_questions
    )
    session.add(result)
    session.commit()
    total_score = QuizResult.get_total_score(session, user_id)
    return result, total_score
