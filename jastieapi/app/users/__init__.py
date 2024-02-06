from . routes import users_router
from jastieapi.app.core import app

app.include_router(users_router)