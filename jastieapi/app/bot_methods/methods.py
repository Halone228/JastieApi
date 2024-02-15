from aiogram import Bot
from pyrogram import Client
from pyrogram.filters import enums
from os import getenv
from aiogram.types import (
    ChatMemberOwner,
    ChatMemberAdministrator,
    ChatMemberMember,
    ChatMemberRestricted,
    ChatMemberLeft,
    ChatMemberBanned
)
from typing import Union

from pyrogram.types import ChatMember, User

from .data_models import *


class BotMethods:
    bot = Bot(getenv("BOT_TOKEN"))
    bot_client: Client

    @classmethod
    async def init(cls):
        cls.bot_client = Client(
            name='main_client',
            api_id=7816785,
            api_hash='a31486c26edf6c02ed37333696a2a49e',
            phone_number='+375298936228'
        )

    @classmethod
    async def get_user(cls, user_id: int, chat_id: int = int(getenv("CHAT_ID"))) -> Union[
        ChatMemberOwner,
        ChatMemberAdministrator,
        ChatMemberMember,
        ChatMemberRestricted,
        ChatMemberLeft,
        ChatMemberBanned,
    ]:
        await cls.bot_client.start()
        return await cls.bot.get_chat_member(chat_id, user_id)

    @classmethod
    async def get_users(
        cls,
        chat_id: int,
        filter: enums.ChatMembersFilter = enums.ChatMembersFilter.SEARCH,
        query: str = None
    ) -> list[User]:
        async with cls.bot_client as bot:
            bot: Client
            return [i.user async for i in bot.get_chat_members(
                    chat_id,
                    query=query,
                    filter=filter
                )
            ]


__all__ = [
    'BotMethods'
]