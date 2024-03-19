from asyncio import gather, sleep

from jastieapi.app.include import *
from .datamodels import *

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


__all__ = [
    'admin_route'
]
