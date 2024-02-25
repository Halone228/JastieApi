from .core import *
from loguru import logger
from time import perf_counter
from gzip import compress


class LoggerMiddleware:
    def __init__(
        self,
        level_name: str,
        level_icon: str,
        **extra
    ):
        self.level = logger.level(
            level_name,
            icon=level_icon,
            no=18
        )
        self.logger = logger.bind(**extra)

    async def __call__(self, request: Request, call_next):
        start_time = perf_counter()
        response: Response = await call_next(request)
        end_time = perf_counter()
        async with context_session() as session:
            logger_helper = LogsDBHelper(session)
            await logger_helper.request_log(
                endpoint=request.url.query,
                time_elapsed=end_time-start_time,
                request_body=await request.body(),
                response_body=response.body,
                response_code=response.status_code,
                method=request.method
            )