import inspect
from datetime import datetime

from loguru import logger

from config import connectToDB


async def parseAllUsers():
    async with connectToDB() as db:
        try:
            select_rest = await db.execute(
                f"SELECT user_id FROM 'users'"
            )
            await db.commit()
            allUsers = await select_rest.fetchall()

            return allUsers
        except Exception as er:
            logger.error(er)
        finally:
            await db.commit()


async def create_new_rest(rest_name):
    async with connectToDB() as db:
        try:
            await db.execute(
                "INSERT INTO 'rests' (name) VALUES (?)",
                (rest_name,)
            )
            print("rest created")
            await db.commit()

            rest_id = await db.execute(
                """SELECT id FROM 'rests' WHERE name = :rest_name""",
                {'rest_name': rest_name}
            )
            await db.commit()
            values = await rest_id.fetchone()

            return values[0]

        except Exception as er:
            logger.error(er)
        finally:
            await db.commit()


async def delete_new_rest(rest_id):
    async with connectToDB() as db:
        try:
            await db.execute(
                "DELETE FROM modules WHERE id = (?)",
                (rest_id,)
            )
        except Exception as er:
            logger.error(er)
        finally:
            await db.commit()


async def add_type_new_rest(rest_id, rest_data, description=None, adress=None, menu=None, avarage_check=None,
                            kitchen=None, rest_type=None, view=None, image=None):
    async with connectToDB() as db:
        try:
            if not description is None:
                dbQuery = f'description'

            elif not adress is None:
                dbQuery = f'address'

            elif not menu is None:
                dbQuery = f'menu'

            elif not avarage_check is None:
                dbQuery = f'avarage_check'

            elif not kitchen is None:
                dbQuery = f'kitchen'

            elif not rest_type is None:
                dbQuery = f'rest_type'

            elif not view is None:
                dbQuery = f'view'

            elif not image is None:
                dbQuery = f'image'

            await db.execute(
                f"UPDATE 'users' SET {dbQuery} = :rest_data WHERE rest_id = :rest_id",
                {'rest_data': rest_data, 'rest_id': rest_id}
            )
        except Exception as er:
            logger.error(er)
        finally:
            await db.commit()
