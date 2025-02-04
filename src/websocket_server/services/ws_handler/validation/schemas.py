import datetime

from pydantic import BaseModel, Field
from pydantic.networks import IPvAnyNetwork

from src.static_schemas.static import (
    TypeCommand,
    TypeModeRouteMap,
    TypePacket,
    TypePower,
    TypeSignal,
    TypeSignalDetection,
)


class UnknownTypePacketDTO(BaseModel):
    time: datetime.datetime | None = Field(description="Время", default=None)
    packet_type: int = Field(description="Неизвестный тип пакета", alias="packetType")
    command_uuid: str | None = Field(
        description="Идентификатор команды", alias="commandUUID", default=None
    )


class CommandFrameDTO(BaseModel):
    time: datetime.datetime = Field(description="Время")
    packet_type: TypePacket = Field(description="Тип пакета", alias="packetType")
    id_device: str = Field(
        description="Идентификатор устройства", alias="deviceID", pattern=r"U-\d{10}"
    )
    additional: str | None = Field(description="Дополнительная информация", default=None)
    command: TypeCommand = Field(description="Команда устройству")
    command_uuid: str = Field(description="Идентификатор команды", alias="commandUUID")
    port: int = Field(description="Порт", ge=0, le=65535)
    ip_address: IPvAnyNetwork = Field(description="IP", alias="ipAddress")
    login: str = Field(description="Логин", min_length=1, max_length=64)
    password: str = Field(description="Пароль", min_length=4, max_length=64)


class CommandDetectorIdentsFrameDTO(BaseModel):
    signal_type: TypeSignal | None = Field(description="Тип сигнала", alias="signalType")
    signal_detection_type: TypeSignalDetection | None = Field(
        description="Тип обнаруженного сигнала", alias="signalDetectionType"
    )


class CommandDetectorParamsFrameDTO(BaseModel):
    signal_frequency: int | None = Field(
        description="Частота сигнала", alias="signalFrequency"
    )
    signal_amplitude: int | None = Field(
        description="Амплитуда сигнала", alias="signalAmplitude", ge=-150, le=20
    )
    signal_width: int | None = Field(description="Ширина сигнала", alias="signalWidth")
    idents: CommandDetectorIdentsFrameDTO


class CommandDetectorFrameDTO(CommandFrameDTO):
    params: CommandDetectorParamsFrameDTO


class CommandEmtRouteMapIntermediateCoordinateDTO(BaseModel):
    latitude: float = Field(description="Широта", ge=-90.0, le=90.0)
    longitude: float = Field(description="Долгота", ge=-90.0, le=90.0)


class CommandEmitRouteMapDTO(BaseModel):
    route_map_id: int = Field(description="Идентификатор маршрута", alias="routeMapId")
    power: TypePower = Field(description="Мощность")
    mode_route_map: TypeModeRouteMap = Field(
        description="Режим работы маршрута", alias="modeRouteMap"
    )
    altitude: int = Field(description="Высота", ge=0)
    speed: int = Field(description="Скорость", ge=0)
    duration: int = Field(description="Продолжительность", ge=0)
    start_latitude: float = Field(
        description="Стартовая широта", alias="startLatitude", ge=-90.0, le=90.0
    )
    start_longitude: float = Field(
        description="Стартовая долгота", alias="startLongitude", ge=-90.0, le=90.0
    )
    finish_latitude: float = Field(
        description="Финишная широта", alias="finishLatitude", ge=-90.0, le=90.0
    )
    finish_longitude: float = Field(
        description="Финишная долгота", alias="finishLongitude", ge=-90.0, le=90.0
    )
    intermediate_coordinate: list[CommandEmtRouteMapIntermediateCoordinateDTO] = Field(
        alias="intermediateCoordinate"
    )


class CommandSpoofingFrameDTO(CommandFrameDTO):
    delay: int | None = Field(description="Задержка", alias="emitDelay")
    route_map: list[CommandEmitRouteMapDTO] = Field(
        description="Сценарии", alias="emitRouteMap"
    )


class CommandSuppressorFrameDTO(CommandFrameDTO):
    signal_type: TypeSignal | None = Field(default="Тип сигнала", alias="signalType")
    delay: int | None = Field(description="Задержка", alias="emitDelay", ge=0)
    duration: int | None = Field(
        description="Продолжительность", alias="emitDuration", ge=0
    )
    power: TypePower | None = Field(description="Мощность", alias="signalPower")
    channel: list[int] = Field(description="Каналы устройства", alias="fixFrequencies")
