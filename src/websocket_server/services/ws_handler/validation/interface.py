from abc import ABC, abstractmethod

from pydantic import BaseModel


class IWsServerPacketValidation(ABC):

    @abstractmethod
    def validate(self, data: dict) -> BaseModel: ...
