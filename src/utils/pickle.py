import os
import pickle


def _load_data(path_to_file: str) -> dict:
    with open(path_to_file, "rb") as read_file:
        return pickle.load(read_file)


def _dump_data(path_to_file: str, data: dict) -> None:
    with open(path_to_file, "wb") as write_file:
        pickle.dump(data, write_file)


def create_file_with_test_data(path_to_file: str) -> None:
    """Создаёт файл с тестовыми данными"""
    _dump_data(path_to_file, {"test": "test"})


def is_file_exist(path_to_file: str) -> bool:
    """Проверяет существование файла"""
    return os.path.isfile(path_to_file)


def get_data_by_key_from_file(path_to_file: str, key: str) -> str | None:
    """Получает данные по ключу"""
    data: dict = _load_data(path_to_file)
    return data.get(key, None)


def get_all_data_from_file(path_to_file: str) -> dict:
    """Получение всех пар ключ-значение из файла"""
    return _load_data(path_to_file)


def delete_data_by_key_from_file(path_to_file: str, key: str) -> None:
    """Удаляет значение по ключу"""
    data: dict = _load_data(path_to_file)
    if key in data:
        data.pop(key)
        _dump_data(path_to_file, data)


def add_new_data_by_key_to_file(path_to_file: str, key: str, value: str) -> None:
    """Добавляет значение по ключу"""
    data: dict = _load_data(path_to_file)
    data[key] = value
    _dump_data(path_to_file, data)
