from .vendors import *
from .skins import *
from .users import *
from .core import app as main_router
from .matches import *
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from jastiedatabase.sql import init_db
from jastiedatabase.redis import get_discounts, get_discount
from jastiedatabase.redis.methods import Discount
from pydantic import BaseModel


class DiscountsAnswer(BaseModel):
    data: list[Discount]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


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