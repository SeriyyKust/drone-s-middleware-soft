import datetime
import uuid

from fastapi import WebSocket


class WSBaseManagerConsumer:

    def __init__(self):
        self._active_connections: dict[str, WebSocket] = {}

    @staticmethod
    def _get_time() -> str:
        return str(datetime.datetime.now())

    def _create_connect_frame(self, client_id: str) -> dict:
        return {"time": self._get_time(), "client_id": client_id}

    async def connect(self, websocket: WebSocket) -> str:
        await websocket.accept()
        client_id = str(uuid.uuid1())
        self._active_connections[client_id] = websocket
        await websocket.send_json(self._create_connect_frame(client_id))
        return client_id

    def disconnect(self, client_id: str):
        self._active_connections.pop(client_id)

    async def receive(self, client_id: str) -> dict:
        return await self._active_connections[client_id].receive_json()

    async def send_personal_message(self, message_data: dict, client_id: str):
        await self._active_connections[client_id].send_json(message_data)

    async def broadcast(self, message_data: dict):
        for key in self._active_connections.keys():
            await self._active_connections[key].send_json(message_data)


base_websocket_manager_consumer = WSBaseManagerConsumer()
