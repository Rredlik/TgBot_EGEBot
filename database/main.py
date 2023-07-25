from typing import Final

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from misc.singleton import SingletonMeta


class Database:  # metaclass=SingletonMeta
    Base: Final = declarative_base()

    def __init__(self):
        self.__session = None
        self.__engine = None

    # def __getattr__(self, name):
    #     return getattr(self.__session, name)

    async def init(self):
        self.__engine = create_async_engine(
            url='sqlite+aiosqlite:///database.db',
            echo=True, future=True
        )
        self.__session = sessionmaker(
            bind=self.__engine, expire_on_commit=False, class_=AsyncSession
        )

    async def create_all(self):
        async with self.__engine.begin() as conn:
            await conn.run_sync(Database.Base.metadata.create_all)

    # async def session(self):
    #     async with self.__session as session:
    #         async with session.begin():
    #             return session
    #
    # @property
    # def engine(self):
    #     return self.__engine


async_db_session = Database()


async def register_database():
    await async_db_session.init()
    await async_db_session.create_all()
#
# async def register_db():
#     async with Database().engine as conn:
#         await conn.run_sync(Database.BASE.metadata.create_all)

# async def db_session():
#     async_session = sessionmaker(bind=Database.engine,
#                                  expire_on_commit=False, class_=AsyncSession)
