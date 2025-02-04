from abc import ABC, abstractmethod
from typing import Iterable


class IManagerTelegramUsers(ABC):

    @abstractmethod
    async def get_able_users_id(self) -> Iterable[int]: ...

    @abstractmethod
    async def set_able_user(self, user_id: int) -> None: ...

    @abstractmethod
    async def set_disable_user(self, user_id: int) -> None: ...
