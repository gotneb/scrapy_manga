from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv
from .entities import Manga
from .database import Database

load_dotenv()


class MangaDatabase(Database):
    def __init__(self) -> None:
        self.client = None
        self.database = None
        self.mangas = None

    def add(self, manga: Manga) -> str:
        try:
            results = self.mangas.insert_one(manga.to_dict())
            return results.inserted_id
        except Exception as error:
            print(error)
            return None

    def remove(self, url: str) -> bool:
        try:
            results = self.mangas.delete_one({"url": url})
            return results.deleted_count == 1
        except Exception as error:
            print(error)
            return False

    def get(self, url: str) -> Manga:
        try:
            results = self.mangas.find_one({"url": url})
            manga = Manga.dict_to_manga(results)
            return manga
        except Exception as error:
            print(error)
            return None

    def set(self, url: str, manga: Manga) -> bool:
        try:
            results = self.mangas.update_one({"url": url}, {"$set": manga.to_dict()})
            return results.matched_count == 1
        except Exception as error:
            print(error)
            return False

    def search(self, title: str) -> list[Manga]:
        try:
            results = []
            cursor = self.mangas.find({"$text": {"$search": title}})
            for doc in cursor:
                results.append(Manga.dict_to_manga(doc))
            return results
        except Exception as error:
            print(error)
            return None

    def exists(self, url: str) -> bool:
        return self.mangas.find_one({"url": url}) != None

    def is_empty(self, origin: str = None) -> bool:
        if origin == "readm":
            return self.mangas.count_documents({"origin": "readm"}) == 0
        elif origin == "manga_livre":
            return self.mangas.count_documents({"origin": "manga_livre"}) == 0

        return self.mangas.count_documents({}) == 0

    def connect(self) -> bool:
        try:
            self.client: MongoClient = MongoClient(getenv("MONGO_URI"))
            self.database = self.client.get_database("manga_db")
            self.mangas = self.database.get_collection("mangas")

            return True
        except Exception as error:
            print(error)
            return False

    def close(self) -> None:
        if self.client:
            self.client.close()
