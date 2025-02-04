import logging
from typing import Iterable

from src.utils import pickle

from .interface import IManagerTelegramUsers


_logger = logging.getLogger(__name__)


class PickleManagerTelegramUsers(IManagerTelegramUsers):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._filename: str = "users.pickle"
        if not pickle.is_file_exist(self._filename):
            pickle.create_file_with_test_data(self._filename)

    async def get_able_users_id(self) -> Iterable[int]:
        data: dict = pickle.get_all_data_from_file(self._filename)
        return filter(lambda x: data[x] == "able", data.keys())

    async def set_able_user(self, user_id: int) -> None:
        _logger.debug("Start, user_id = %s", user_id)
        pickle.add_new_data_by_key_to_file(
            path_to_file=self._filename, key=str(user_id), value="able"
        )

    async def set_disable_user(self, user_id: int) -> None:
        _logger.debug("Start, user_id = %s", user_id)
        pickle.add_new_data_by_key_to_file(
            path_to_file=self._filename, key=str(user_id), value="disable"
        )
