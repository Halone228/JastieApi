from jastieapi.app.include import *
from jastiedatabase.redis.methods import url_exists, add_skin as redis_add_skin
from .client import get_skin_from_url
from jastiedatabase.datamodels import Skin

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


@skins_routes.post('/add')
async def add_skin(
    url: Annotated[str, Body()],
    price: Annotated[float, Body()]
):
    if await url_exists(url):
        raise HTTPException(
            status_code=409,
            detail='Already exists'
        )
    skin_data = await get_skin_from_url(url)
    if not skin_data:
        raise HTTPException(
            status_code=418,
            detail='Cant get skin'
        )
    skin_data['price'] = price
    RunnerSaver.create_task(redis_add_skin(
        Skin.model_validate(
            skin_data
        )
    ))
