import uuid
from asyncio import gather, sleep
from io import BytesIO

from fastapi import UploadFile, Form, File
from jastieapi.app.include import *
from .datamodels import *
from jastiedatabase.redis import redis_client
from uuid import uuid4

admin_route = APIRouter(
    prefix='/admin',
    tags=['admin']
)


@admin_route.post('/send_all_text')
async def send_message_text(
    data: TextMessage,
    users_db_helper: users_db_typevar
):
    send_message = BotMethods.no_peer_invalid(BotMethods.send_message)
    all_users = list(await users_db_helper.get_all_users_ids())
    for chunk in chunks(all_users, 50):
        await gather(
            *[send_message(id_, data.text) for id_ in chunk]
        )
        await sleep(.6)


@admin_route.post('/send_all_image')
async def send_message_image(
    users_db_helper: users_db_typevar,
    caption: Annotated[str, Form()],
    file: Annotated[UploadFile, File()] = None,
):
    send_image = BotMethods.no_peer_invalid(BotMethods.send_image)
    bytio = BytesIO(await file.read())
    bytio.name = file.filename + '.jpg'
    all_users = list(await users_db_helper.get_all_users_ids())
    for chunk in chunks(all_users, 25):
        await gather(
            *[send_image(id_, image=bytio, caption=caption) for id_ in chunk]
        )
        await sleep(.6)


@admin_route.post(
    '/send_all_image_gift'
)
async def send_message_image_gift(
    users_db_helper: users_db_typevar,
    caption: Annotated[str, Form()],
    gift_size: Annotated[int, Form()],
    button_text: Annotated[str, Form()],
    file: Annotated[UploadFile, File()] = None
):
    send_image = BotMethods.no_peer_invalid(BotMethods.send_gift)
    bytio = BytesIO(await file.read())
    bytio.name = file.filename + '.jpg'
    all_users = tuple(await users_db_helper.get_all_users_ids())
    gift_id = uuid.uuid4()
    await redis_client.set(f'gift_{gift_id}', gift_size)
    
    async def send_messages():
        for chunk in chunks(all_users, 30):
            await gather(
                *[send_image(id_, image=bytio, caption=caption, button_text=button_text, gift_id=gift_id) for id_ in chunk]
            )
    RunnerSaver.create_task(send_messages())


@admin_route.post(
    '/add_gift',
)
async def add_gift(
    users_db_helper: users_db_typevar,
    user_id: Annotated[int, Body()],
    gift_id: Annotated[str, Body()]
):
    if not await redis_client.exists(f'{gift_id}:{user_id}') and await redis_client.exists(f'gift_{gift_id}'):
        points = int(await redis_client.get(f'gift_{gift_id}') or 0)
        await users_db_helper.add_points(
            user_id,
            points,
            f'gift-{gift_id}'
        )
        await redis_client.set(f'{gift_id}:{user_id}', 0)
        await BotMethods.send_message(
            user_id,
            f'Вы получили {points} баллов, в качестве вознаграждения'
        )

__all__ = [
    'admin_route'
]
