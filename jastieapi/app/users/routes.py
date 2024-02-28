from asyncio import gather

import os
from fastapi import Query

from jastieapi.app.include import *
from .datamodels import *
from jastieapi.app.bot_methods import *
from jastieapi.app.bot_methods.methods import BotMethods

users_router = APIRouter(
    prefix='/users',
    tags=['User']
)


class PointsAdd(BaseModel):
    points: float


@users_router.get('/add/{chat_id}/{user_id}')
async def add_user(
    chat_id: int,
    user_id: int,
    db_helper_users: users_db_typevar
):
    if chat_id != user_id and chat_id not in config.ALLOWED_CHATS:
        raise CHAT_DISALLOWED

    await db_helper_users.add_user(
        user_id
    )


@users_router.get('/info/{chat_id}/{user_id}')
async def get_user(
    chat_id: int,
    user_id: int
):
    return BotMethods.get_user(user_id, chat_id)


@users_router.get(
    '/points/{user_id}',
    responses={
        **response_des
    }
)
async def get_user_points(
    user_id: int,
    db_helper_users: users_db_typevar
) -> Points:
    await found_user(user_id, db_helper_users)
    return Points(
        points=await db_helper_users.get_points(user_id),
        user_id=user_id
    )


@users_router.post('/points/users')
async def get_users_points_bulk(
    db_helper_users: users_db_typevar,
    user_ids: Annotated[list[int], Body()]
):
    data = await db_helper_users.get_users_points(user_ids)
    return {
        i.user_id: i.points for i in data
    }


@users_router.post('/new_message')
async def new_message(
    message: MessageValue,
    db_helper_users: users_db_typevar
):
    logger.debug(message)
    if message.chat_id not in config.ALLOWED_CHATS:
        raise CHAT_DISALLOWED

    RunnerSaver.create_task(db_helper_users.new_message(message.text, message.user_id, message.message_id))


@users_router.get('/add_referrer/{user_id}/{referrer_id}')
async def add_referrer(
    user_id: int,
    referrer_id: int,
    db_users_helper: users_db_typevar
) -> ReferrerAnswer:
    result = await db_users_helper.add_referrer(user_id, referrer_id)
    if result == -1:
        return ReferrerAnswer(
            code=UsersResultCodes.REFERRER_ALREADY_EXISTS
        )
    if result == 1:
        return ReferrerAnswer(
            code=UsersResultCodes.REFERRER_SELF
        )
    return ReferrerAnswer(
        code=UsersResultCodes.SUCCESS
    )


@users_router.get('/referrers_count/{user_id}')
async def get_referrers_count(
    user_id: int,
    users_db_helper: users_db_typevar
):
    return {
        'data': await users_db_helper.get_referrals_count(user_id)
    }


@users_router.get('/find')
async def find_users(
    query: str
) -> UsersList:
    return UsersList.model_validate(
        {'result': await BotMethods.get_users(chat_id=int(os.getenv('CHAT_ID')), query=query)},
        from_attributes=True,
        strict=False
    )


@users_router.post('/add/{user_id}')
async def add_user_points(
    user_id: int,
    data: PointsAdd,
    users_db_helper: users_db_typevar
):
    RunnerSaver.create_task(users_db_helper.add_points(user_id, data.points, by="api-admin"))
