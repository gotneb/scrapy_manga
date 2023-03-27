from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv
from .entities import Manga

load_dotenv()


class MangaDatabase:
    def __init__(self) -> None:
        self.uri = getenv("MONGO_URI")
        self.client = None
        self.database = None
        self.collection = None

    def add(self, manga: Manga) -> str:
        """Insert a new manga in database and returns an id"""
        try:
            if self.exists_by_manga(manga):
                raise Exception(f"Document with title {manga.title} already exists.")

            results = self.collection.insert_one(manga.to_dict())
            return results.inserted_id
        except Exception as error:
            print(error)
            return None

    def exists_by_manga(self, manga: Manga):
        """Checks if manga already exists"""
        return (
            self.collection.find_one(
                {
                    "title": manga.title,
                    "origin": manga.origin,
                    "language": manga.language,
                }
            )
            != None
        )

    def connect(self) -> bool:
        """Connect to database and returns True if sucessful"""
        try:
            self.client: MongoClient = MongoClient(self.uri)
            self.database = self.client["manga_db"]
            self.collection = self.database["mangas"]

            return True
        except Exception as error:
            print(error)
            return False

    def close(self) -> None:
        """Close database conncetion"""
        if self.client:
            self.client.close()
