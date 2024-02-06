from jastieapi.app import *


def start_dev():
    import uvicorn
    uvicorn.run(
        app
    )
