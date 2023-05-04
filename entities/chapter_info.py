from dataclasses import dataclass
from .entity import Entity


@dataclass
class ChapterInfo(Entity):
    name: str
    id: str = None

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name}
