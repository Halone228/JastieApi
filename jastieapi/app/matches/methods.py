from jastieapi.app.bot_methods import BotMethods
from asyncio import gather


async def send_messages(users_message: dict):
    task = gather(*[
        BotMethods.bot_client.send_message(
          chat_id=k, text=v
        ) for k, v in users_message.items()
    ])
    await task
