import datetime

from pydantic import BaseModel, Field, field_validator

from src.static_schemas import TypeBlock, TypeCommand, TypeFrame


class UnknownTypeFrameDTO(BaseModel):
    time: datetime.datetime | None = Field(description="Время", default=None)
    type_frame: str = Field(description="Полученный тип пакета")


class MessageFrameDTO(BaseModel):
    time: datetime.datetime = Field(description="Время")
    type_frame: TypeFrame = Field(description="Тип пакета")


class GeneralNotificationDataDTO(BaseModel):
    text: str = Field(description="Текст уведомления", min_length=1)


class GeneralNotificationDTO(MessageFrameDTO):
    data: GeneralNotificationDataDTO = Field(description="Тело уведомления")

    @classmethod
    @field_validator("type_frame")
    def check_type_frame(cls, type_frame: TypeFrame) -> TypeFrame:
        if type_frame != TypeFrame.GENERAL_NOTIFICATION:
            raise ValueError("type_frame должен иметь значение GENERAL_NOTIFICATION.")
        return type_frame


class BlockNotificationData(BaseModel):
    type_block: TypeBlock = Field(description="Тип блока")
    type_block_title: str = Field(description="Тип блока (название)", min_length=1)
    text: str = Field(description="Текст уведомления")
    enable_text_notifications: bool = Field(description="Включить текстовое уведомление")
    enable_sound_notifications: bool = Field(description="Включить звуковое уведомление")


class BaseBlockNotificationDTO(MessageFrameDTO):
    data: BlockNotificationData


class BlockNotificationDTO(BaseBlockNotificationDTO):

    @classmethod
    @field_validator("type_frame")
    def check_type_frame(cls, type_frame: TypeFrame) -> TypeFrame:
        if type_frame != TypeFrame.BLOCK_NOTIFICATION:
            raise ValueError("type_frame должен иметь значение BLOCK_NOTIFICATION.")
        return type_frame


class ErrorBlockNotificationDTO(BaseBlockNotificationDTO):

    @classmethod
    @field_validator("type_frame")
    def check_type_frame(cls, type_frame: TypeFrame) -> TypeFrame:
        if type_frame != TypeFrame.ERROR_BLOCK_NOTIFICATION:
            raise ValueError("type_frame должен иметь значение ERROR_BLOCK_NOTIFICATION.")
        return type_frame


class ConfirmationDataDTO(BaseModel):
    id: str = Field(description="Идентификатор подтверждения")
    type_block: TypeBlock = Field(description="Тип блока")
    type_block_title: str = Field(description="Тип блока (название)", min_length=1)
    command: TypeCommand = Field(description="Команда")
    command_title: str = Field(description="Команда (название)", min_length=1)
    duration: int = Field(description="Время выполнения", ge=0)
    wait_to_complete: bool = Field(description="Ожидать завершения выполнения команды")


class ConfirmationDTO(MessageFrameDTO):
    data: ConfirmationDataDTO

    @classmethod
    @field_validator("type_frame")
    def check_type_frame(cls, type_frame: TypeFrame) -> TypeFrame:
        if type_frame != TypeFrame.CONFIRMATION:
            raise ValueError("type_frame должен иметь значение CONFIRMATION.")
        return type_frame
