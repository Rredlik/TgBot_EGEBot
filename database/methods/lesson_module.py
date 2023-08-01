from loguru import logger

from config import connectToDB


async def get_one(name):
    async with connectToDB() as db:
        try:
            command = await db.execute(
                """SELECT * FROM 'storage_modules' where name = :name""",
                {'name': name})
            modules = await command.fetchone()
            return modules
        except Exception as er:
            logger.error(f"{er}")
        finally:
            await db.commit()


async def get_all():
    async with connectToDB() as db:
        try:
            command = await db.execute(
                """SELECT * FROM 'storage_modules'"""
            )
            modules = await command.fetchall()
            return modules
        except Exception as er:
            logger.error(f"{er}")
        finally:
            await db.commit()
# async def add_module(user_id):
#     async with connectToDB() as db:
#         stage = (await get(user_id)) + 1
#         try:
#             await db.execute(
#                 f"UPDATE 'users' SET stage = :stage WHERE user_id = :user_id",
#                 {'user_id': user_id, 'stage': stage}
#             )
#             await db.commit()
#         except Exception as er:
#             logger.error(f"{er}")
#         finally:
#             await db.commit()
