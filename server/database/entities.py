from dataclasses import dataclass
from abc import abstractclassmethod, ABC


class Entity(ABC):
    @abstractclassmethod
    def to_dict(self) -> dict:
        pass


@dataclass
class Chapter(Entity):
    name: str
    pages: list[str]

    def to_dict(self) -> dict:
        return {"name": self.name, "pages": self.pages}


@dataclass
class ChapterInfo(Entity):
    id: str
    name: str

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name}


@dataclass
class Manga(Entity):
    """Class used to stored manga in the database"""

    title: str
    alternative_title: str
    author: str
    artist: str
    status: str
    url: str
    origin: str
    language: str
    thumbnail: str
    genres: list[str]
    summary: str
    chapters: list[Chapter] | None
    chapters_info: list[ChapterInfo] | None

    def chapters_to_dict_list(self):
        if self.chapters:
            return list(map(lambda chapter: chapter.to_dict(), self.chapters))
        else:
            return []

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "alternative_title": self.alternative_title,
            "author": self.author,
            "artist": self.artist,
            "status": self.status,
            "url": self.url,
            "origin": self.origin,
            "language": self.language,
            "thumbnail": self.thumbnail,
            "genres": self.genres,
            "summary": self.summary,
            "chapters": self.chapters_to_dict_list(),
        }

    def get_chapter_names(self) -> list[str]:
        return list(map(lambda chapter: chapter.name, self.chapters))


@dataclass
class WebsiteUpdate(Entity):
    origin: str
    populars: list[str]
    latest_updates: list[str]

    def to_string(self):
        return {
            "origin": self.origin,
            "populars": self.populars,
            "latest_updates": self.latest_updates,
        }
