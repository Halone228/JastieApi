import asyncio
import os
from asyncio import Task
from contextlib import asynccontextmanager

import loguru
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from dateutil.parser.isoparser import isoparse
from jastieapi.app.bot_methods.methods import BotMethods
from jastieapi.app.middlewares import middlewares
from jastiedatabase.redis.methods import Discount
from jastiedatabase.sql.methods.users import increment_count
from jastiedatabase.redis import redis_client
from .core import app as main_router
from .matches import *
from .skins import *
from .users import *
from .vendors import *
from aioschedule import every, run_pending


class DiscountsAnswer(BaseModel):
    data: list[Discount]


tasks: set[Task] = set()


@asynccontextmanager
async def lifespan(app: FastAPI):
    @loguru.logger.catch()
    async def forward_message():
        if ((raw_data := await redis_client.get('next_message_datetime')) is not None
            and isoparse(raw_data.decode()) > datetime.now()):
            return
        await redis_client.set('next_message_datetime', (datetime.now() + timedelta(weeks=1)).isoformat())
        loguru.logger.debug('Forwarding message')
        await BotMethods.forward_message(
            chat_id=int(os.getenv('CHAT_ID')),
            message_id=int(os.getenv("MESSAGE_ID")),
            from_chat_id=int(os.getenv("FROM_CHAT_ID"))
        )

    await gather(BotMethods.init(), init_db())

    async def increment_loop():
        loguru.logger.debug('Start increment loop')
        while True:
            await asyncio.sleep(20)
            # await forward_message()
            async with context_session() as session:
                await increment_count(session)

    if not os.getenv('TEST'):
        task = asyncio.create_task(increment_loop())
    yield


app = FastAPI(
    host='0.0.0.0',
    port=5000,
    lifespan=lifespan
)
app.include_router(main_router)
for middleware in middlewares:
    app.middleware('http')(middleware)


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
