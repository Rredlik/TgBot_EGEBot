import os
from abc import ABC
from typing import Final
from dotenv import load_dotenv


class Env(ABC):
    load_dotenv()
    BOT_TOKEN: Final = os.environ.get('BOT_TOKEN', 'define me!')