from pydantic import BaseModel
from aiogram import types


class ChatMembersResult(BaseModel):
    result: list[types.ChatMemberMember]


__all__ = [
    'ChatMembersResult'
]