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
    await BotMethods.init()

    async def increment_loop():
        loguru.logger.debug('Start increment loop')
        async with context_session() as session:
            while True:
                await asyncio.sleep(20)
                await increment_count(session)
    await init_db()
    task = asyncio.create_task(increment_loop())
    yield
    del task


app = FastAPI(
    host='0.0.0.0',
    port=5000,
    lifespan=lifespan
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