from loguru import logger

from config import connectToDB


async def parseAllUsers():
    async with connectToDB() as db:
        try:
            select_rest = await db.execute(
                f"SELECT user_id FROM 'storage_users'"
            )
            await db.commit()
            allUsers = await select_rest.fetchall()

            return allUsers
        except Exception as er:
            logger.error(er)
        finally:
            await db.commit()
