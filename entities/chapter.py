from dataclasses import dataclass
from .entity import Entity


class Chapter(Entity):
    def __init__(self, name: str, pages: list[str] = [], id: str | None = None) -> None:
        self.name: str = name
        self.pages: list[str] = pages
        self.id: str | None = id

    def to_dict(self) -> dict:
        return {"name": self.name, "pages": self.pages}

    def is_empty(self) -> bool:
        return len(self.pages) == 0
