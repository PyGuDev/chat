import aioredis
from aioredis.client import PubSub

import settings


class RedisBackand:
    def __init__(self):
        self._host = settings.REDIS_HOST
        self._port = settings.REDIS_PORT
        self._pass = settings.REDIS_PASS
        self._connection = aioredis.Redis(host=self._host, port=self._port, password=self._pass)

    async def subscribe(self, channel_name: str) -> PubSub:
        channel: PubSub = self._connection.pubsub()
        await channel.subscribe(channel_name)
        return channel

    async def publish(self, channel_name: str, message: str):
        await self._connection.publish(channel_name, message)
