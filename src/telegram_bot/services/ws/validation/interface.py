from abc import ABC, abstractmethod

from pydantic import BaseModel


class IValidationWSData(ABC):

    @abstractmethod
    def validate(self, data: dict) -> BaseModel: ...
