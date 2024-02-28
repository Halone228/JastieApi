import os
from pytest import fixture, mark
from httpx import AsyncClient
from jastieapi.app import *
from asgi_lifespan import LifespanManager


pytestmark = mark.asyncio


@fixture(scope='session')
def chat_id():
    return int(os.getenv('CHAT_ID'))


@fixture(scope='session')
def user_id():
    return 5645972090


@fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@fixture(autouse=True, scope='session')
def bot_token():
    return os.getenv('BOT_TOKEN')


@fixture(scope='session', autouse=True)
async def client(anyio_backend):
    async with LifespanManager(app) as manager:
        async with AsyncClient(app=manager.app, base_url='http://test') as cli:
            yield cli

