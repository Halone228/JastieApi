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
from .data_models import *


class BotMethods:
    bot = Bot(getenv("BOT_TOKEN"))
    bot_client = Client(name='main_bot', bot_token=getenv("BOT_TOKEN"))

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
        filter: enums.ChatMembersFilter = None,
        query: str = None
    ) -> ChatMembersResult:
        return ChatMembersResult.model_validate(
        {
                'result': cls.bot_client.get_chat_members(
                    chat_id,
                    query=query,
                    filter=filter
                )
            },
            from_attributes=True
        )

__all__ = [
    'BotMethods'
]