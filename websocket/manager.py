from typing import List

from fastapi import WebSocket

from websocket.backands import RedisBackand


class ChannelManager(RedisBackand):
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self._channels = {}
        super().__init__()

    async def subscribe_channel(self, name: str):
        prefix_name = self._add_prefix_to_name(name)
        return await self.subscribe(prefix_name)

    @staticmethod
    def _add_prefix_to_name(name: str) -> str:
        return f"channel:{name}"

    async def send(self, channel_name: str, message: str):
        prefix_name = self._add_prefix_to_name(channel_name)
        await self.publish(prefix_name, message)
