from dataclasses import dataclass
from entities import Entity


@dataclass
class WebsiteUpdate(Entity):
    origin: str
    populars: list[str]
    language: str

    def to_dict(self):
        return {
            "origin": self.origin,
            "populars": self.populars,
            "language": self.language,
        }
