import os

from dotenv import load_dotenv
from pytest import fixture


@fixture(scope='session')
def chat_id():
    return int(os.getenv('CHAT_ID'))
