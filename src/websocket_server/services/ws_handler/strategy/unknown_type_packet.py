import datetime

from ..validation.schemas import UnknownTypePacketDTO
from .interface import IPacketHandlerStrategy


class UnknownTypeWsServerPacketStrategy(IPacketHandlerStrategy):

    @staticmethod
    def _get_time_now() -> str:
        return str(datetime.datetime.now())

    async def execute(self, dto: UnknownTypePacketDTO) -> dict:
        return {
            "time": self._get_time_now(),
            "packetType": 22,  # TODO: Должен быть пакет ошибки
            "receivedType": f"{dto.packet_type}",
            "receivedCommandUUID": dto.command_uuid,
            "description": f"Был получен пакет неизвестный тип пакета {dto.packet_type}",
        }
