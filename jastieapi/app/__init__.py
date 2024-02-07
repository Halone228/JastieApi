from .vendors import *
from .skins import *
from .users import *
from .core import app as main_router
from .matches import *
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from jastie_database.sql import init_db


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


__all__ = [
    'app'
]