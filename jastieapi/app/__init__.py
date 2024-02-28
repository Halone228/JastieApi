import asyncio

import loguru

from .vendors import *
from .skins import *
from .users import *
from .core import app as main_router
from .matches import *
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from jastiedatabase.sql import init_db
from jastiedatabase.sql.methods.users import increment_count
from jastiedatabase.sql.methods import context_session
from jastiedatabase.redis import get_discounts, get_discount
from jastiedatabase.redis.methods import Discount
from jastieapi.app.bot_methods.methods import BotMethods
from pydantic import BaseModel


class DiscountsAnswer(BaseModel):
    data: list[Discount]


@asynccontextmanager
async def lifespan(app: FastAPI):
    _ = asyncio.create_task(BotMethods.init())
    __ = asyncio.create_task(init_db())

    async def increment_loop():
        loguru.logger.debug('Start increment loop')
        while True:
            await asyncio.sleep(20)
            async with context_session() as session:
                await increment_count(session)
    task = asyncio.create_task(increment_loop())
    await __
    await _
    yield
    del task


app = FastAPI(
    host='0.0.0.0',
    port=5000,
    lifespan=lifespan,
    debug=True
)
app.include_router(main_router)


@app.get('/')
async def index() -> RedirectResponse:
    return RedirectResponse(
        url='/docs'
    )


@app.get('/discounts/all')
async def get_discounts_() -> DiscountsAnswer:
    return DiscountsAnswer(
        data=await get_discounts()
    )


@app.get('/discounts/{discount_uid:str}')
async def get_discount(discount_uid: str) -> Discount:
    return await get_discount(discount_uid)


__all__ = [
    'app'
]