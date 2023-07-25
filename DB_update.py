import asyncio
import inspect
import time
from datetime import datetime

from config import connectToDB


# import aiomysql


# async def connectToDB():
#     connect = await aiomysql.connect(host='127.0.0.1', port=3306,
#                                       user='root', password='',
#                                       db='mysql', loop=loop)
#     return connect
#
#
# async def update_full_description_MYSQL(all_db=True, rest_id=None):
#     time_start = time.time()
#     connection = await connectToDB()
#     async with connection as db:
#         # await db.executemany()
#         try:
#             if all_db:
#                 values = await db.execute(
#                     """SELECT name FROM 'rests'"""
#                 )
#                 restaurants = await values.fetchall()
#             else:
#                 values = await db.execute(
#                     """SELECT name FROM 'rests' WHERE id = :rest_id""",
#                     {'rest_id': rest_id}
#                 )
#                 restaurants = await values.fetchall()
#             print(f'1 [DB info] for {time.time() - time_start:0.3f} seconds')
#             for rest in restaurants:
#                 d = await db.execute(
#                     """SELECT name, description, address, menu, average_check, kitchen, rest_type, view
#                     FROM 'rests' WHERE name = :name""",
#                     {'name': rest[0]}
#                 )
#                 name, description, address, menu, average_check, kitchen, rest_type, view = await d.fetchone()
#
#                 if not (name is None or name == ''):
#                     desc_text = f'<b>{name}</b> '
#
#                     if not (rest_type is None or rest_type == ''):
#                         desc_text += f'({rest_type})\n\n'
#                     else:
#                         desc_text += '\n\n'
#
#                 if not (kitchen is None or kitchen == ''):
#                     desc_text += f'🍴Кухня: {kitchen}\n\n'
#
#                 if not (description is None or description == ''):
#                     desc_text += f'{description}\n\n'
#
#                 if (not menu is None or menu == ''):
#                     desc_text += f'🍽️<a href="{menu}">Меню</a>\n'
#
#                 if not (view is None or view == ''):
#                     desc_text += f'👀<a href="{view}">Обзор</a>\n'
#
#                 if not (average_check is None or average_check == ''):
#                     desc_text += f'🧾Ср.Чек ~ {average_check}₽\n'
#
#                 if not (address is None or address == ''):
#                     desc_text += f'🗺️Адрес: {address}'
#
#
#                 await db.execute(
#                     f"UPDATE 'rests' SET full_description = :desc_text,"
#                     f" small_name = :sname WHERE name = :name;",
#                     {'desc_text': desc_text, 'name': name, 'sname': name.lower()}
#                 )
#
#                 await db.commit()
#             print(f'2 [DB info] for {time.time() - time_start:0.3f} seconds')
#
#         except Exception as er:
#             print(f'[[ERROR]{datetime.now()} {inspect.getframeinfo(inspect.currentframe()).function}]: {er}')
#         else:
#             await db.commit()
#         print(f'3 [DB info] for {time.time() - time_start:0.3f} seconds')
#     print(f'4 [DB info] for {time.time() - time_start:0.3f} seconds')


async def update_full_description(all_db=True, rest_id=None):
    time_start = time.time()

    async with connectToDB() as db:
        # await db.executemany()
        try:
            if all_db:
                values = await db.execute(
                    """SELECT name FROM modules"""
                )
                restaurants = await values.fetchall()
            else:
                values = await db.execute(
                    """SELECT name FROM 'rests' WHERE id = :rest_id""",
                    {'rest_id': rest_id}
                )
                restaurants = await values.fetchall()
            print(f'1 [DB info] for {time.time() - time_start:0.3f} seconds')
            for rest in restaurants:
                d = await db.execute(
                    """SELECT name, description, address, addres_link, menu, average_check, 
                        kitchen, rest_type, view, phone_number 
                        FROM modules WHERE name = :name""",
                    {'name': rest[0]}
                )
                name, description, address, address_link, menu, average_check, \
                    kitchen, rest_type, view, phone_number = await d.fetchone()

                if not (name is None or name == ''):
                    desc_text = f'<b>{name}</b> '

                    if not (rest_type is None or rest_type == ''):
                        desc_text += f'({rest_type})\n\n'
                    else:
                        desc_text += '\n\n'

                if not (kitchen is None or kitchen == ''):
                    desc_text += f'🍴Кухня: {kitchen}\n\n'

                if not (description is None or description == ''):
                    desc_text += f'{description}\n\n'

                if not menu is None or menu == '':
                    desc_text += f'🍽️<a href="{menu}">Меню</a>\n'

                if not (view is None or view == ''):
                    desc_text += f'👀<a href="{view}">Обзор</a>\n'

                if not (average_check is None or average_check == ''):
                    desc_text += f'🧾Ср.Чек ~ {average_check}₽\n'

                if not (address is None or address == ''):
                    desc_text += '🗺️Адрес: '
                    address = address.split(';')
                    address_link = address_link.split(';')
                    for i in range(len(address)):
                        addAddress = address[i].strip()
                        addAddress_link = address_link[i].strip()
                        desc_text += f'<a href="{addAddress_link}">{addAddress}</a>\n'

                if not (phone_number is None):
                    desc_text += f"☎️ "
                    phone_number = phone_number.split(';')
                    for i in range(len(phone_number)):
                        addNumb = phone_number[i].strip()
                        desc_text += f'<code>{addNumb}</code>\n'

                await db.execute(
                    f"UPDATE 'rests' SET full_description = :desc_text,"
                    f" small_name = :sname WHERE name = :name;",
                    {'desc_text': desc_text, 'name': name, 'sname': name.lower()}
                )

                await db.commit()
            print(f'2 [DB info] for {time.time() - time_start:0.3f} seconds')

        except Exception as er:
            print(f'[[ERROR]{datetime.now()} {inspect.getframeinfo(inspect.currentframe()).function}]: {er}')
        else:
            await db.commit()
        print(f'3 [DB info] for {time.time() - time_start:0.3f} seconds')
    print(f'4 [DB info] for {time.time() - time_start:0.3f} seconds')


async def get_full_description(rest_id):
    async with connectToDB() as db:
        try:
            select_rest = await db.execute(
                f"SELECT name, full_description, image FROM modules WHERE row_number() = (:rest_id)" ,
                {'rest_id': rest_id}
            )
            await db.commit()
            rest = await select_rest.fetchone()

            return rest
        except Exception as er:
            print(f'[[ERROR]{datetime.now()} {inspect.getframeinfo(inspect.currentframe()).function}]: {er}')
        finally:
            await db.commit()


if __name__ == "__main__":
    # category = "eijlk"
    # request_txt = (f"""SELECT full_description FROM rests WHERE :filter = 1""", {":filter": category})
    (asyncio.run(update_full_description()))
    # print(request_txt)
