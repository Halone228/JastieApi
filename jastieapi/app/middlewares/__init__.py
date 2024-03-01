from .logger import *

middlewares = [
    LoggerMiddleware("MIDDLEWARE", "M",
                     ['/users/new_message', '/docs', '/openapi.json'])
]

__all__ = [
    'middlewares'
]
