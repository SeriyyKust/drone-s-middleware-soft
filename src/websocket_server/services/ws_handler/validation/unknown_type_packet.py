from .interface import IWsServerPacketValidation
from .schemas import UnknownTypePacketDTO


class UnknownTypedWsServerPacketValidation(IWsServerPacketValidation):

    def validate(self, data: dict) -> UnknownTypePacketDTO:
        return UnknownTypePacketDTO.model_validate(data)
