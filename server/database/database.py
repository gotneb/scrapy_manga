from abc import ABC, abstractclassmethod
from .entities import Manga


class Database(ABC):
    """A base (abstract) class for building the database."""

    @abstractclassmethod
    def add(self, manga: Manga) -> str:
        """Insert a new manga in database and returns an id"""
        pass

    @abstractclassmethod
    def remove(self, url: str) -> bool:
        """Delete document with same id in database"""
        pass

    @abstractclassmethod
    def get(self, url: str) -> Manga:
        """Returns document with same url"""
        pass

    @abstractclassmethod
    def set(self, url: str, manga: Manga) -> bool:
        """Change manga with same url"""
        pass

    @abstractclassmethod
    def search(self, title: str) -> list[Manga]:
        """Return mangas with similar titles or alternative titles"""
        pass

    @abstractclassmethod
    def exists(self, url: str) -> bool:
        """Checks if manga already exists by id"""
        pass

    @abstractclassmethod
    def is_empty(self, origin: str = None) -> bool:
        """Return true if docs with same origin exists. If origin is None, return True if mangas 'mangas' is empty"""
        pass

    @abstractclassmethod
    def connect(self) -> bool:
        """Connect to database and returns True if sucessful"""
        pass

    @abstractclassmethod
    def close(self) -> None:
        """Close database conncetion"""
        pass
