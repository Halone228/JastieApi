from jastieapi.app.core import app
from .routes import *

app.include_router(matches_router)
