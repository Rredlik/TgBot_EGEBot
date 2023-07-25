import os
from abc import ABC
from typing import Final
from dotenv import load_dotenv
TOKEN = '5526113848:AAHXJKLH5BEDyogSFUbaupnrE1H2NoehBoI'

class Env(ABC):
    load_dotenv()
    TOKEN: Final = os.environ.get('TOKEN', 'define me!')