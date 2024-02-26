from jastiedatabase.sql import UserDBHelper
from typing import NoReturn
from fastapi import HTTPException
from asyncio import Task, Future, create_task
from types import CoroutineType
from inspect import iscoroutine


class RunnerSaver:
    tasks = set()

    @classmethod
    def create_task(cls, task: Task | Future | CoroutineType):
        if iscoroutine(task):
            task = create_task(task)
        cls.tasks.add(task)
        task.add_done_callback(cls.tasks.discard)


user_not_found = HTTPException(
    status_code=404,
    detail='User not found'
)
response_des = {
    404: {'description': 'User not found'}
}


async def found_user(user_id: int, db_helper: UserDBHelper):
    if await db_helper.get_user(user_id) is None:
        raise user_not_found


__all__ = [
    'found_user',
    'response_des',
    'RunnerSaver'
]