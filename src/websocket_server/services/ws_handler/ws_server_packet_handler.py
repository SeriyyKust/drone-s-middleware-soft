from pydantic import BaseModel

from src.websocket_server.services.ws_handler.strategy import IPacketHandlerStrategy
from src.websocket_server.services.ws_handler.strategy.command import (
    CommandWsServerPacketStrategy,
)
from src.websocket_server.services.ws_handler.strategy.unknown_type_packet import (
    UnknownTypeWsServerPacketStrategy,
)
from src.websocket_server.services.ws_handler.validation import IWsServerPacketValidation
from src.websocket_server.services.ws_handler.validation.command import (
    DetectorCommandWsServerPacketValidation,
    SpoofingCommandWsServerPacketValidation,
    SuppressorCommandWsServerPacketValidation,
)
from src.websocket_server.services.ws_handler.validation.unknown_type_packet import (
    UnknownTypedWsServerPacketValidation,
)


class WsServerPacketHandler:

    def __init__(
        self, validation: IWsServerPacketValidation, strategy: IPacketHandlerStrategy
    ):
        self._validation: IWsServerPacketValidation = validation
        self._strategy: IPacketHandlerStrategy = strategy

    def validate(self, data: dict) -> BaseModel:
        return self._validation.validate(data)

    async def execute(self, dto: BaseModel) -> dict:
        return await self._strategy.execute(dto)


class DetectorCommandWsServerPacketHandler(WsServerPacketHandler):

    def __init__(self):
        super().__init__(
            validation=DetectorCommandWsServerPacketValidation(),
            strategy=CommandWsServerPacketStrategy(),
        )


class SuppressorCommandWsServerPackerHandler(WsServerPacketHandler):

    def __init__(self):
        super().__init__(
            validation=SuppressorCommandWsServerPacketValidation(),
            strategy=CommandWsServerPacketStrategy(),
        )


class SpoofingCommandWsServerPackerHandler(WsServerPacketHandler):

    def __init__(self):
        super().__init__(
            validation=SpoofingCommandWsServerPacketValidation(),
            strategy=CommandWsServerPacketStrategy(),
        )


class UnknownTypeWsServerPackerHandler(WsServerPacketHandler):

    def __init__(self):
        super().__init__(
            validation=UnknownTypedWsServerPacketValidation(),
            strategy=UnknownTypeWsServerPacketStrategy(),
        )
