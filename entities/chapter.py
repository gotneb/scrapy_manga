from dataclasses import dataclass
from .entity import Entity


@dataclass
class Chapter(Entity):
    name: str
    pages: list[str]

    def to_dict(self) -> dict:
        return {"name": self.name, "pages": self.pages}
