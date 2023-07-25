# import aiohttp
import aiosqlite
import pendulum as pendulum
# 5526113848:AAHXJKLH5BEDyogSFUbaupnrE1H2NoehBoI
ADMIN_IDS = [351931465]  # 351931465
CHANNEL_ID = [-1001665320015]  # ачо а ничо
CHANNEL_LINK = "https://t.me/rredlik"
VIDEO_INSTRUCTION_ID = 'BAACAgIAAxkBAAIPXWOrGRg67kqZ__kMkbFPaD2x0fPFAALbIQACW0tZSYGMqlJk_XlbLAQ'


def set_datetime(record):
    record['extra']['datetime'] = pendulum.now('Asia/Yekaterinburg').strftime('%d-%m-%Y %H:%M-%S')


def connectToDB():
    connection = aiosqlite.connect('./main.db')
    return connection

# async def async_gather_http_get():
#     params = {
#         "chat_id": CHAT_ID,
#         "user_id": 5531606682
#     }
#     async with aiohttp.ClientSession() as session:
#         async with session.post(f'https://api.telegram.org/{API_TOKEN}/getChatMember',
#                                 data=params) as response:
#             print("Status:", response.status)
#             print("Content-type:", response.headers['content-type'])
#
#             html = await response.text()
#             print("Body:", html, "...")

#
# if __name__ == '__main__':
#     asyncio.run(async_gather_http_get())
