import loguru
from httpx import AsyncClient, Response
from pytest import mark
from jastieapi.app.users.codes import UsersResultCodes


def resolve_response(response: Response):
    assert 200 >= response.status_code < 300


@mark.dependency(name='add_user')
async def test_add_user(client: AsyncClient, chat_id: int, user_id: int):
    response = await client.get(f'/users/add/{chat_id}/{user_id}')
    resolve_response(response)


@mark.dependency(depends=['add_user'], name='get_points')
async def test_get_points(client: AsyncClient, user_id):
    response = await client.get(f'/users/points/{user_id}')
    resolve_response(response)
    data = response.json()
    assert data['points'] == 0
    assert data['user_id'] == user_id


@mark.dependency(depends=['get_points'], name='add_points')
async def test_add_points(client: AsyncClient, user_id, random_num):
    response = await client.post(f'/users/add/{user_id}', json={'points': random_num})
    resolve_response(response)
    response = await client.get(f'/users/points/{user_id}')
    resolve_response(response)
    data = response.json()
    assert data['points'] == random_num
    response = await client.post(f'/users/add/{user_id}', json={'points': -random_num})
    resolve_response(response)


@mark.dependency(depends=['get_points', 'add_points'], name='new_message')
async def test_new_message(client: AsyncClient, user_id, random_text, symbol_price, chat_id):
    text_len = len(random_text['text'])
    text_price = text_len * symbol_price
    data = random_text
    data['chat_id'] = chat_id
    data['user_id'] = user_id
    response = await client.post('/users/new_message', json=data)
    resolve_response(response)
    response = await client.get(f'/users/points/{user_id}')
    resolve_response(response)
    data = response.json()
    assert round(data['points'], 2) == round(text_price, 2)
    response = await client.post(f'/users/add/{user_id}', json={'points': -data['points']})
    resolve_response(response)


@mark.dependency(depends=['add_user'], name='add_referrer')
async def test_add_referrer(client: AsyncClient, user_id, random_id, chat_id):
    response = await client.get(f'/users/add/{chat_id}/{random_id}')
    resolve_response(response)
    response = await client.get(f'/users/add_referrer/{random_id}/{user_id}')
    resolve_response(response)
    data = response.json()
    assert data['code'] == UsersResultCodes.SUCCESS.value


@mark.dependency(depends=['add_referrer'], name='test_referrals')
async def test_referrals(client: AsyncClient, user_id):
    response = await client.get(f'/users/referrers_count/{user_id}')
    resolve_response(response)
    data = response.json()
    assert data['data'] == 1
