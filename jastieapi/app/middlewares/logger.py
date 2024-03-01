from time import perf_counter

from loguru import logger
from starlette.responses import StreamingResponse
from starlette.concurrency import iterate_in_threadpool
from .core import *


class LoggerMiddleware:
    def __init__(
        self,
        level_name: str,
        level_icon: str,
        exclude_endpoints=None,
        **extra
    ):
        if exclude_endpoints is None:
            exclude_endpoints = list()
        self.level = logger.level(
            level_name,
            icon=level_icon,
            no=18
        )
        self.logger = logger.bind(**extra)
        self.exclude = exclude_endpoints

    async def __call__(self, request: Request, call_next):
        if self.exclude is not None:
            for route in self.exclude:
                if route in request.url.path:
                    return await call_next(request)

        request_body = await request.body()
        start_time = perf_counter()
        response: StreamingResponse = await call_next(request)
        end_time = perf_counter()
        _raw_body = [chunk async for chunk in response.body_iterator]
        response_body = b''.join(_raw_body)
        response.body_iterator = iterate_in_threadpool(iter(_raw_body))

        async with context_session() as session:
            logger_helper = LogsDBHelper(session)
            await logger_helper.request_log(
                endpoint=request.url.path + (f'?{request.url.query}' if request.url.query else ''),
                time_elapsed=end_time - start_time,
                request_body=request_body,
                response_body=response_body,
                response_code=response.status_code,
                method=request.method
            )
        return response
