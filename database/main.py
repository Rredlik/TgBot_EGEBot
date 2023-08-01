from loguru import logger

from config import connectToDB


async def create_db():
    async with connectToDB() as db:

        try:
            dbs = db.execute("PRAGMA table_info(storage_users)").fetchall()
            print(dbs)
            if len(db.execute("PRAGMA table_info(storage_users)").fetchall()) == 3:
                print("DB was found(1/3)")
            else:
                await db.execute('create table storage_users('
                                 'user_id  TEXT not null primary key unique,'
                                 'reg_date INTEGER           not null,'
                                 'stage    INTEGER default 0 not null)')
                print("DB was not found(1/3) | Creating...")

            if len(db.execute("PRAGMA table_info(storage_users)").fetchall()) == 2:
                print("DB was found(2/3)")
            else:
                await db.execute('create table storage_modules('
                                 'id          INTEGER not null primary key autoincrement unique,'
                                 ' name       TEXT,'
                                 'description TEXT,'
                                 'link        TEXT not null)')
                print("DB was not found(2/3) | Creating...")

            if len(db.execute("PRAGMA table_info(storage_users)").fetchall()) == 1:
                print("DB was found(3/3)")
            else:
                await db.execute('create table storage_config('
                                 'setting TEXT,'
                                 'value   TEXT)')
                print("DB was not found(3/3) | Creating...")

        except Exception as er:
            logger.error(f"{er}")
        finally:
            await db.commit()
