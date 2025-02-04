from .interface import IWsServerPacketValidation
from .schemas import (
    CommandDetectorFrameDTO,
    CommandSpoofingFrameDTO,
    CommandSuppressorFrameDTO,
)


class DetectorCommandWsServerPacketValidation(IWsServerPacketValidation):

    def validate(self, data: dict) -> CommandDetectorFrameDTO:
        return CommandDetectorFrameDTO.model_validate(data)


class SuppressorCommandWsServerPacketValidation(IWsServerPacketValidation):

    def validate(self, data: dict) -> CommandSuppressorFrameDTO:
        return CommandSuppressorFrameDTO.model_validate(data)


class SpoofingCommandWsServerPacketValidation(IWsServerPacketValidation):

    def validate(self, data: dict) -> CommandSpoofingFrameDTO:
        return CommandSpoofingFrameDTO.model_validate(data)
