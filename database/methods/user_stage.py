from loguru import logger

from config import connectToDB


async def get(user_id):
    async with connectToDB() as db:
        try:
            command = await db.execute(
                """SELECT stage FROM 'users' WHERE user_id = :user_id""",
                {'user_id': user_id}
            )
            stage = await command.fetchone()
            print(stage)
            return stage[0]
        except Exception as er:
            logger.error(f"{er}")
        finally:
            await db.commit()


async def next(user_id):
    async with connectToDB() as db:
        stage = (await get(user_id)) + 1
        try:
            await db.execute(
                f"UPDATE 'users' SET stage = :stage WHERE user_id = :user_id",
                {'user_id': user_id, 'stage': stage}
            )
            await db.commit()
        except Exception as er:
            logger.error(f"{er}")
        finally:
            await db.commit()
