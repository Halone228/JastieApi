from jastieapi.app.core import app
from .routes import *
app.include_router(skins_routes)