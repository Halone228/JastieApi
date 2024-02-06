from jastieapi.app.include import *
from .datamodels import *

users_router = APIRouter(
    prefix='/users',
    tags=['User']
)


@users_router.get('/add/{chat_id}/{user_id}')
async def add_user(
    chat_id: int,
    user_id: int,
    db_helper_users: Annotated[UserDBHelper, Depends(get_helper(UserDBHelper))]
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


@users_router.get('/points/{user_id}')
async def get_user_points(
    user_id: int,
    db_helper_users: Annotated[UserDBHelper, Depends(get_helper(UserDBHelper))]
) -> Points:
    return Points(
        points=await db_helper_users.get_points(user_id),
        user_id=user_id
    )


@users_router.post('/new_message')
async def new_message(
    message: aiogram_types.Message,
    db_helper_users: Annotated[UserDBHelper, Depends(get_helper(UserDBHelper))]
):
    if message.chat.id not in config.ALLOWED_CHATS:
        raise CHAT_DISALLOWED

    await db_helper_users.new_message(message)

