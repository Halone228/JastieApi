from pydantic import BaseModel
from .codes import UsersResultCodes


class Points(BaseModel):
    points: float
    user_id: int


class MessageValue(BaseModel):
    text: str
    user_id: int
    chat_id: int


class ReferrerAnswer(BaseModel):
    code: UsersResultCodes
