from src.utils import pickle

from .interface import ICheckConfirmation


class PickleCheckConfirmation(ICheckConfirmation):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._filename: str = "confirm.pickle"
        if not pickle.is_file_exist(self._filename):
            pickle.create_file_with_test_data(self._filename)

    async def get(self, confirm_uuid: str) -> bool | None:
        value = pickle.get_data_by_key_from_file(self._filename, confirm_uuid)
        return value == "confirm" if value is not None else None

    async def set(self, confirm_uuid: str, confirm: bool) -> None:
        pickle.add_new_data_by_key_to_file(
            path_to_file=self._filename,
            key=confirm_uuid,
            value="confirm" if confirm else "non_confirm",
        )
