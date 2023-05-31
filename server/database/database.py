from abc import ABC, abstractclassmethod
from entities import Manga, WebsiteUpdate
from bson import ObjectId


class Database(ABC):
    """A base (abstract) class for building the database."""

    @abstractclassmethod
    def add(self, manga: Manga) -> ObjectId:
        """Insert a new manga in database and returns an id"""
        pass

    @abstractclassmethod
    def add_all(self, mangas: list[Manga]) -> list[ObjectId]:
        """Insert a manga list  in database and returns an list with inserted ids"""
        pass

    @abstractclassmethod
    def remove(self, url: str) -> bool:
        """Delete document with same url in database"""
        pass

    @abstractclassmethod
    def remove_all(self, urls: list[str]) -> bool:
        """Delete all documents with same urls"""
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
    def search(self, search_term: str) -> list[dict]:
        """Return mangas with similar titles or alternative titles"""
        pass

    @abstractclassmethod
    def exists(self, url: str) -> bool:
        """Checks if manga already exists by id"""
        pass

    @abstractclassmethod
    def list_genres(self, language: str) -> list[str]:
        """Returns a list with genres (by language: english or portuguese)"""
        pass

    @abstractclassmethod
    def get_mangas_by_genre(self, genre: str) -> list[dict]:
        """Returns a list with mangas"""
        pass

    @abstractclassmethod
    def get_populars(self, origin: str) -> list[dict]:
        """Return a list od the most popular mangas"""
        pass

    @abstractclassmethod
    def get_latest_updates(self, origin: str) -> list[dict]:
        """Return a list of recently updated mangas"""
        pass

    @abstractclassmethod
    def add_update_info(self, update: WebsiteUpdate) -> ObjectId:
        """Add website info"""
        pass

    @abstractclassmethod
    def remove_update_info(self, origin: str) -> bool:
        """Remove website info"""
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
    def connect(self, mongo_uri: str) -> bool:
        """Connect to database and returns True if sucessful"""
        pass

    @abstractclassmethod
    def close(self) -> None:
        """Close database conncetion"""
        pass
