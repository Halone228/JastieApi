from jastieapi.app.bot_methods import BotMethods
from loguru import logger


async def test_search_users(chat_id):
    data = await BotMethods.get_users(chat_id, query='Kirill')
    assert 5645972090 in [i.id for i in data]
