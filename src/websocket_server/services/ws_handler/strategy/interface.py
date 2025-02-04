from abc import ABC, abstractmethod

from pydantic import BaseModel


class IPacketHandlerStrategy(ABC):

    @abstractmethod
    async def execute(self, dto: BaseModel) -> dict: ...
