from .vendors import *
from .skins import *
from .users import *
from .core import app as main_router
from .matches import *
from fastapi import FastAPI
from fastapi.responses import RedirectResponse


app = FastAPI(
    host='0.0.0.0',
    port=5000
)
app.include_router(main_router)


@app.get('/')
async def index():
    return RedirectResponse(
        url='/docs'
    )


__all__ = [
    'app'
]