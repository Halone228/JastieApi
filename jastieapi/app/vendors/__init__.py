from jastieapi.app.core import app
from .routes import *
app.include_router(vendors_route)