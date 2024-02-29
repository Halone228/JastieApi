from jastieapi.app import *
from subprocess import run


def start_dev():
    run(["uvicorn", 'main:app', '--reload', '--host', '0.0.0.0'])


def start_prod():
    import uvicorn
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=5000
    )


def start_test():
    from pytest import main
    main(['tests', "-v", "-s", "-W", "ignore::pytest.PytestAssertRewriteWarning"])

