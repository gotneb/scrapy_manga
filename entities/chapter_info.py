from dataclasses import dataclass
from .entity import Entity


@dataclass
class ChapterInfo(Entity):
    id: str
    name: str

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name}
