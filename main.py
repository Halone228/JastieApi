from jastieapi.app import *


def start_dev():
    import uvicorn
    uvicorn.run(
        app,
        host='0.0.0.0'
    )


def start_prod():
    import uvicorn
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=5000
    )


def start_test():
    from pytest import main
    main('tests')