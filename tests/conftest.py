import asyncio
import os
from pytest import fixture
from httpx import AsyncClient
from jastieapi.app import *
from asgi_lifespan import LifespanManager
from essential_generators import DocumentGenerator

pytest_plugins = ('pytest_asyncio',)
gen = DocumentGenerator()


@fixture(scope='session')
def chat_id():
    return int(os.getenv('CHAT_ID'))


@fixture(scope='session')
def user_id():
    return 5645972090


@fixture(autouse=True, scope='session')
def bot_token():
    return os.getenv('BOT_TOKEN')


@fixture(scope='function')
def random_num():
    import random
    return random.randint(100, 500)


@fixture(scope='function')
def random_id():
    return gen.integer() % 10000000


@fixture(scope='function')
def random_text():
    return {
        'text': gen.sentence(),
        'message_id': gen.integer()
    }


@fixture(scope='session')
def symbol_price():
    return 0.01


@fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@fixture(scope='session')
async def client():
    async with LifespanManager(app) as manager:
        async with AsyncClient(app=manager.app, base_url='http://test') as cli:
            yield cli
