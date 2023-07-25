from sqlalchemy import Column, Integer, String
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from .main import Database, async_db_session


class ModelAdmin:
    @classmethod
    async def create(cls):
        async_db_session.add(cls)
        await async_db_session.commit()

    @classmethod
    async def update(cls, **kwargs):
        query = (
            sqlalchemy_update(User)
            .where(**kwargs)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await async_db_session.execute(query)
        await async_db_session.commit()

    @classmethod
    async def get_one(cls, **kwargs):
        query = select(cls).where(cls.telegam_id == id)
        results = await async_db_session.execute(query)
        (result,) = results.one()
        return result

    @classmethod
    async def get_all(cls, **kwargs):
        query = select(cls).where(**kwargs)
        results = await async_db_session.execute(query)
        (result,) = results.all()
        return result


class User(Database.Base, ModelAdmin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False)
    favourite_rests = Column(Integer, nullable=False)
    admin = Column(Integer, default=0)
    # session = relationship('Session', uselist=False, backref="USER", passive_deletes=True)
    # payment = relationship('Payment', uselist=False, backref="USER", passive_deletes=True)


class Rests(Database.Base, ModelAdmin):
    __tablename__ = 'rests'
    id                  = Column(Integer, primary_key=True)
    full_name           = Column(String, nullable=False)
    description         = Column(String, nullable=False)
    address             = Column(String, nullable=False)
    menu                = Column(String, nullable=False)
    average_check       = Column(Integer, nullable=False)
    kitchen             = Column(String, nullable=False)
    rest_type           = Column(String, nullable=False)
    view                = Column(String, nullable=False)
    small_name          = Column(String, nullable=False)
    full_description    = Column(String, nullable=False)
    image               = Column(String, nullable=False)
    fav_points          = Column(Integer, nullable=False, default=0)
    window_view         = Column(Integer, nullable=False, default=0)
    interior            = Column(Integer, nullable=False, default=0)
    parking             = Column(Integer, nullable=False, default=0)
    child_room          = Column(Integer, nullable=False, default=0)
    chamber             = Column(Integer, nullable=False, default=0)
    family              = Column(Integer, nullable=False, default=0)
    meeting             = Column(Integer, nullable=False, default=0)
    working             = Column(Integer, nullable=False, default=0)
    company_party       = Column(Integer, nullable=False, default=0)
    birth_day           = Column(Integer, nullable=False, default=0)
    break_fast          = Column(Integer, nullable=False, default=0)
    party               = Column(Integer, nullable=False, default=0)
    pre_party           = Column(Integer, nullable=False, default=0)
    proper_nutrition    = Column(Integer, nullable=False, default=0)


class ConfigData(Database.Base, ModelAdmin):
    __tablename__ = 'config'
    setting_name = Column(String, nullable=False, primary_key=True)
    value = Column(Integer, nullable=False)


# class Session(Database.BASE):
#     __tablename__ = 'SESSION'
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('USER.id', ondelete='CASCADE'), unique=True)
#     string = Column(String, nullable=False)
#     enable = Column(Integer, default=0)
#
#
# class Payment(Database.BASE):
#     __tablename__ = 'PAYMENT'
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('USER.id', ondelete='CASCADE'), unique=True)
#     key = Column(String, unique=True)


# async def register_models():
#     async with Database().engine as conn:
#         await conn.run_sync(Database.BASE.metadata.create_all)
