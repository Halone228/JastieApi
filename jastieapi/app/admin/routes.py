import uuid
from asyncio import gather, sleep
from io import BytesIO

from fastapi import UploadFile, Form, File, Query
from jastieapi.app.include import *
from .datamodels import *
from pydantic import BaseModel
from jastiedatabase.datamodels import BidFull, Operation

admin_route = APIRouter(
    prefix='/admin',
    tags=['admin']
)


class BidsStatistics(BaseModel):
    match_id: int
    match_sum: float
    match_count: int


class Pagination(BaseModel):
    page: Annotated[int, Query(ge=0)]
    limit: Annotated[int, Query(gt=1)]


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


@admin_route.get(
    '/bids_statistics',
    response_model=list[BidsStatistics]
)
async def get_bids_statistics(
    matches_db_helper: matches_db_typevar
):
    return await matches_db_helper.get_matches_statistics()


@admin_route.get(
    '/bids',
    response_model=list[BidFull]
)
async def get_bids(
    pagination: Annotated[Pagination, Depends()],
    matches_db_helper: matches_db_typevar
):
    return TypeAdapter(list[BidFull]).validate_python(
        await matches_db_helper.get_paginated_bids(pagination.page, pagination.limit),
        from_attributes=True
    )


@admin_route.get(
    '/operations',
    response_model=list[Operation]
)
async def get_operation(
    pagination: Annotated[Pagination, Depends()],
    logs_db_helper: logs_db_typevar
):
    operations = await logs_db_helper.get_operations(page=pagination.page, limit=pagination.limit)
    return operations


__all__ = [
    'admin_route'
]
