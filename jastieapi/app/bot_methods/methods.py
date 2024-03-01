import os

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
    async def get_jastie_username(cls):
        return (await cls.get_user(
            int(os.getenv('CHAT_ID')),
            454999432
        )).user.username

    @classmethod
    async def init(cls):
        cls.bot_client = Client(
            name=getenv('SESSION_NAME'),
            api_id=7816785,
            api_hash='a31486c26edf6c02ed37333696a2a49e',
            bot_token=getenv('BOT_TOKEN'),
        )
        await cls.bot_client.start()

    @classmethod
    async def get_user(cls, user_id: int, chat_id: int = int(getenv("CHAT_ID"))) -> Union[
        ChatMemberOwner,
        ChatMemberAdministrator,
        ChatMemberMember,
        ChatMemberRestricted,
        ChatMemberLeft,
        ChatMemberBanned,
    ]:
        return await cls.bot.get_chat_member(chat_id, user_id)

    @classmethod
    async def get_users(
        cls,
        chat_id: int,
        filter: enums.ChatMembersFilter = enums.ChatMembersFilter.SEARCH,
        query: str = None
    ) -> list[User]:
        await cls.bot_client.resolve_peer(chat_id)
        return [i.user async for i in cls.bot_client.get_chat_members(
            chat_id,
            query=query,
            filter=filter
        )
                ]

    @classmethod
    async def forward_message(
        cls,
        chat_id: int,
        message_id: int,
        from_chat_id: int
    ):
        await cls.bot_client.forward_messages(
            chat_id,
            from_chat_id,
            message_id
        )


__all__ = [
    'BotMethods'
]
