import os
from abc import ABC
from typing import Final
from dotenv import load_dotenv


class Env(ABC):
    load_dotenv()
    TOKEN: Final = os.environ.get('TOKEN', 'define me!')