from database.models import User
from database.main import Database
from database.methods.get import get_user_by_telegram_id


def is_vip(telegram_id) -> bool:
    return bool(Database().session.query(User.vip).filter(User.telegram_id == telegram_id).one()[0])


def is_admin(telegram_id: int) -> bool:
    return bool(Database().session.query(User.admin).filter(User.telegram_id == telegram_id).one()[0])


def switch_vip(telegram_id: int):
    user = get_user_by_telegram_id(telegram_id)
    if user:
        user.vip = not user.vip
        Database().session.commit()
