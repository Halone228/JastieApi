from aiohttp import ClientSession
from bs4 import BeautifulSoup
from asyncio import sleep
from jastiedatabase.redis.methods import incr_skin_id


async def get_skin_from_url(url, try_=0):
    if try_ > 5:
        return None
    async with ClientSession() as session:
        try:
            async with session.get(url, params={
                'l': 'russian'
            }) as response:
                soup = BeautifulSoup(await response.text())
                await sleep(0)
                image_src = soup.select_one('.market_listing_largeimage>img').get('src')
                await sleep(0)
                item_name = soup.select('.market_listing_item_name')[-1].text.strip()
                await sleep(0)
                item_id = await incr_skin_id()
                return {
                    'id': item_id,
                    'item_name': item_name,
                    'url': url,
                    'image_src': image_src
                }
        except Exception as e:
            return await get_skin_from_url(url, try_+1)
