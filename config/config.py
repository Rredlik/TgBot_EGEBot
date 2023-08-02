# import aiohttp
import aiosqlite
import pendulum as pendulum





ADMIN_IDS = [351931465]  # 351931465
ADMIN_LINK = ['@skidikis']

CHANNEL_ID = [-1001665320015]  # ачо а ничо
CHANNEL_LINK = "https://t.me/rredlik"

VIDEO_INSTRUCTION_ID = 'BAACAgIAAxkBAAIPXWOrGRg67kqZ__kMkbFPaD2x0fPFAALbIQACW0tZSYGMqlJk_XlbLAQ'


def set_datetime(record):
    record['extra']['datetime'] = pendulum.now('Asia/Yekaterinburg').strftime('%d-%m-%Y %H:%M:%S')


PATH_DATABASE = "database/main.db"
def connectToDB():
    connection = aiosqlite.connect(PATH_DATABASE)
    return connection
