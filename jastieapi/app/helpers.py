from jastiedatabase.sql import UserDBHelper
from typing import NoReturn
from fastapi import HTTPException


user_not_found = HTTPException(
    status_code=404,
    detail='User not found'
)
response_des = {
    404: {'description': 'User not found'}
}


async def found_user(user_id: int, db_helper: UserDBHelper):
    if await db_helper.get_user(user_id) is None:
        raise user_not_found


__all__ = [
    'found_user',
    'response_des'
]