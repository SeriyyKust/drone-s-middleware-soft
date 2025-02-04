from abc import ABC, abstractmethod


class ICheckConfirmation(ABC):

    @abstractmethod
    async def get(self, confirm_uuid: str) -> bool | None: ...

    @abstractmethod
    async def set(self, confirm_uuid: str, confirm: bool) -> None: ...
