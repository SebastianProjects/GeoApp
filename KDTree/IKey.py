from abc import ABC, abstractmethod


class IKey(ABC):
    @abstractmethod
    def compare(self, dimension: int, key: "IKey") -> int:
        pass
