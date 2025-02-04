import asyncio
import datetime
import random
import time
from abc import ABC

from src.core.settings import app_config
from src.static_schemas import TypeDevice, TypeResultExecute

from ..validation.schemas import CommandFrameDTO
from .interface import IPacketHandlerStrategy


class AbstractCommandWsServerPacketStrategy(ABC):

    @staticmethod
    def _get_time_now() -> str:
        return str(datetime.datetime.now())

    @classmethod
    def _create_response_frame(
        cls,
        id_device: str,
        type_device: TypeDevice,
        confirm_time: float,
        result: TypeResultExecute,
        result_text: dict,
        command_uuid: str,
    ) -> dict:
        return {
            "time": cls._get_time_now(),
            "packetType": 18,
            "deviceID": id_device,
            "deviceType": type_device.value,
            "confirmCmdTime": confirm_time,
            "result": result.value,
            "resultText": result_text,
            "commandUUID": command_uuid,
        }


class CommandWsServerPacketStrategy(
    IPacketHandlerStrategy, AbstractCommandWsServerPacketStrategy
):

    async def execute(self, dto: CommandFrameDTO) -> dict:
        start_time = time.time()
        if random.random() < app_config.probability_success_command:
            result = TypeResultExecute.OK
            result_text = {}
        else:
            result = TypeResultExecute.ERROR
            result_text = {"errors": "Внутренняя ошибка устройства"}
        await asyncio.sleep(random.randint(1, 5))
        return self._create_response_frame(
            id_device=dto.id_device,
            type_device=TypeDevice.DETECTOR,  # TODO: Статики, необходимо добавить выбор
            command_uuid=dto.command_uuid,
            confirm_time=time.time() - start_time,
            result=result,
            result_text=result_text,
        )
