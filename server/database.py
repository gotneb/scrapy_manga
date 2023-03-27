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

    def exists(self, manga: Manga):
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
        try:
            self.client: MongoClient = MongoClient(self.uri)
            self.database = self.client["manga_db"]
            self.collection = self.database["mangas"]

            return True
        except Exception as error:
            print(error)
            return False

    def close(self) -> None:
        if self.client:
            self.client.close()
