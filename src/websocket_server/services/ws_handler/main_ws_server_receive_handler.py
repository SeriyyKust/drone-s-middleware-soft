import logging

from src.static_schemas import TypePacket
from src.websocket_server.services.ws_handler.ws_server_packet_handler import (
    DetectorCommandWsServerPacketHandler,
    SpoofingCommandWsServerPackerHandler,
    SuppressorCommandWsServerPackerHandler,
    UnknownTypeWsServerPackerHandler,
    WsServerPacketHandler,
)

from .interface import IWsServerReceiveHandler


_logger = logging.getLogger(__name__)


class WsServerReceiveHandler(IWsServerReceiveHandler):

    @classmethod
    def _create_handler(cls, packet_type: int) -> WsServerPacketHandler:
        if packet_type == TypePacket.DETECTOR_CONTROL_COMMAND.value:
            return DetectorCommandWsServerPacketHandler()
        elif packet_type == TypePacket.SUPPRESSOR_CONTROL_COMMAND.value:
            return SuppressorCommandWsServerPackerHandler()
        elif packet_type == TypePacket.SPOOFING_CONTROL_COMMAND.value:
            return SpoofingCommandWsServerPackerHandler()
        else:
            return UnknownTypeWsServerPackerHandler()

    @classmethod
    def _get_packet_type(cls, data: dict) -> int | None:
        _logger.debug("Start, data = %s", data)
        if "packetType" in data:
            if isinstance(data["packetType"], int):
                return data["packetType"]
            else:
                _logger.warning("packetType имеет тип %s", type(data["packetType"]))
        else:
            _logger.warning("packetType отсутствует в data")
        return None

    async def execute(self, data: dict) -> dict:
        _logger.debug("Start, data = %s", data)
        type_frame = self._get_packet_type(data)
        if type_frame is not None:
            executor: WsServerPacketHandler = self._create_handler(type_frame)
            try:
                model = executor.validate(data)
                response_data = await executor.execute(dto=model)
            except Exception as err:
                _logger.warning(
                    msg="Во время обработки пакета полученного от веб-сокет "
                    "клиента произошла ошибка",
                    exc_info=err,
                )
            else:
                return response_data
        return {}
