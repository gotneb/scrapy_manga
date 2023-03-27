from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv

load_dotenv()


class MangaDatabase:
    def __init__(self) -> None:
        self.uri = getenv("MONGO_URI")
        self.client: MongoClient = MongoClient(self.uri)
        self.db = self.client["manga_db"]
        self.manga_col = self.db["mangas"]
