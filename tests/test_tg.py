from jastieapi.app.bot_methods import BotMethods
from loguru import logger


async def test_search_users(chat_id):
    await BotMethods.init()
    data = await BotMethods.get_users(chat_id, query='Kirill')
    logger.debug(data)
    assert 5645972090 in [i.user.id for i in data]