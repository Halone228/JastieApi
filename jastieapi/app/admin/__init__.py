from .routes import *
from jastieapi.app.core import app

app.include_router(admin_route)
