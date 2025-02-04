from .interface import IValidationWSData
from .schemas import UnknownTypeFrameDTO


class UnknownTypeFrameValidationData(IValidationWSData):

    def validate(self, data: dict) -> UnknownTypeFrameDTO:
        return UnknownTypeFrameDTO.model_validate(data)
