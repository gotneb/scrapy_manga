from abc import abstractclassmethod, ABC


class Entity(ABC):
    @abstractclassmethod
    def to_dict(self) -> dict:
        pass
