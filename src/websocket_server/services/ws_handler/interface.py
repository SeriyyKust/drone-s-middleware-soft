from abc import ABC, abstractmethod


class IWsServerReceiveHandler(ABC):

    @abstractmethod
    async def execute(self, data: dict) -> dict: ...
