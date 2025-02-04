from .interface import IValidationWSData
from .schemas import (
    BlockNotificationDTO,
    ErrorBlockNotificationDTO,
    GeneralNotificationDTO,
)


class GeneralNotificationValidationData(IValidationWSData):

    def validate(self, data: dict) -> GeneralNotificationDTO:
        return GeneralNotificationDTO.model_validate(data)


class BlockNotificationValidationData(IValidationWSData):

    def validate(self, data: dict) -> BlockNotificationDTO:
        return BlockNotificationDTO.model_validate(data)


class ErrorBlockNotificationValidationData(IValidationWSData):

    def validate(self, data: dict) -> ErrorBlockNotificationDTO:
        return ErrorBlockNotificationDTO.model_validate(data)
