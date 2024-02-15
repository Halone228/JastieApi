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


class User(BaseModel):
    id: int
    username: str | None
    first_name: str | None
    last_name: str | None


class UsersList(BaseModel):
    result: list[User]
