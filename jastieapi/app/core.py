from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from aiocache import Cache, RedisCache
from jastiedatabase.redis.core import HOST, PASSWORD, PORT, USER

cache = Cache(
    Cache.REDIS,
    endpoint=HOST,
    port=PORT,
    password=PASSWORD,
    namespace='cached'
)
app = APIRouter()

