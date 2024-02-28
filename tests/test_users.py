import loguru
from httpx import AsyncClient, Response
from pytest import mark


def resolve_status(response: Response):
    assert 200 >= response.status_code < 300


@mark.dependency(name='add_user')
async def test_add_user(client: AsyncClient, chat_id: int, user_id: int):
    response = await client.get(f'/users/add/{chat_id}/{user_id}')
    resolve_status(response)
