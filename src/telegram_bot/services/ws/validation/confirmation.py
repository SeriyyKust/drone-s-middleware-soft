from .interface import IValidationWSData
from .schemas import ConfirmationDTO


class ConfirmationValidationData(IValidationWSData):
    def validate(self, data: dict) -> ConfirmationDTO:
        return ConfirmationDTO.model_validate(data)
