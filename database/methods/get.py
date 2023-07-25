from sqlalchemy import exc

from database.main import Database, async_db_session
from database.models import User


async def get_user_by_telegram_id(telegram_id: int) -> User | None:
    try:
        return await User.get_one(telegram_id=telegram_id)
        # return await Database().session.query(User).filter(User.telegram_id == telegram_id).one()
    except exc.NoResultFound:
        return None


# def get_users_with_sessions() -> list[User]:
#     return Database().session.query(User).filter(User.session).all()


def get_all_telegram_id() -> list[tuple[int]]:
    return Database().session.query(User.telegram_id).all()


def get_user_count() -> int:
    return Database().session.query(User).filter(User.admin == 0).count()


def get_sessions_count() -> int:
    return Database().session.query(User.session).join(User.session).where(User.admin == 0).count()


# def get_sessions_enable_count(vip: bool) -> int:
#     return Database().session.query(User).filter(
#         User.vip == int(vip),
#         User.admin == 0,
#         User.session.has(Session.enable == 1)
#     ).count()
