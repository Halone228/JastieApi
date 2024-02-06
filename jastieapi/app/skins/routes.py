from jastieapi.app.include import *

skins_routes = APIRouter(
    prefix='/skins',
    tags=['Skins']
)


@skins_routes.get('/all')
async def get_skins_paginate(page: int = 0):
    skins = await get_all_skins(page)
    return skins


@skins_routes.get('/{skin_id}')
async def get_skin(skin_id: int):
    skin = await get_skin_by_id(skin_id)
    return skin
