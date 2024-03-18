from time import perf_counter
from fastapi.responses import JSONResponse
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
        extra['level'] = self.level
        self.logger = logger.bind(**extra)
        self.exclude = exclude_endpoints

    async def __call__(self, request: Request, call_next):
        if self.exclude is not None:
            for route in self.exclude:
                if route in request.url.path:
                    return await call_next(request)

        request_body = await request.body()
        raised_exception = None
        response = None  # noqa
        start_time = perf_counter()
        try:
            response: StreamingResponse = await call_next(request)
        except Exception as e:
            raised_exception = e
        end_time = perf_counter()
        if raised_exception is None:
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
        else:
            async with context_session() as session:
                logger_helper = LogsDBHelper(session)
                code = await logger_helper.catch_error(
                    raised_exception
                )
                self.logger.exception(raised_exception)
                return JSONResponse(
                    status_code=500,
                    content={'detail': {
                        'error_code': code
                    }}
                )
