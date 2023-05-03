from abc import ABC, abstractclassmethod
from .entities import Manga, WebsiteUpdate
from bson import ObjectId


class Database(ABC):
    """A base (abstract) class for building the database."""

    @abstractclassmethod
    def add(self, manga: Manga) -> ObjectId:
        """Insert a new manga in database and returns an id"""
        pass

    @abstractclassmethod
    def get(self, url: str) -> dict:
        """Returns document with same url"""
        pass

    @abstractclassmethod
    def set(self, url: str, manga: Manga) -> bool:
        """Change manga with same url"""
        pass

    @abstractclassmethod
    def exists(self, url: str) -> bool:
        """Checks if manga already exists by id"""
        pass

    @abstractclassmethod
    def add_update_info(self, update: WebsiteUpdate) -> ObjectId:
        """Add website info"""
        pass

    @abstractclassmethod
    def get_update_info(self, origin: str) -> dict:
        """Get website update info"""
        pass

    @abstractclassmethod
    def set_update_info(self, update: WebsiteUpdate) -> bool:
        """Updates website info"""
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
