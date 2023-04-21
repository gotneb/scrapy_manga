from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv
from .entities import Manga

load_dotenv()


class MangaDatabase:
    def __init__(self) -> None:
        self.client = None
        self.database = None
        self.mangas = None

    def add(self, manga: Manga) -> str:
        """Insert a new manga in database and returns an id"""
        try:
            results = self.mangas.insert_one(manga.to_dict())
            return results.inserted_id
        except Exception as error:
            print(error)
            return None

    def remove(self, url: str) -> bool:
        """Delete document with same id in database"""
        try:
            results = self.mangas.delete_one({"url": url})
            return results.deleted_count == 1
        except Exception as error:
            print(error)
            return False

    def get(self, url: str) -> Manga:
        """Returns document with same url"""
        try:
            results = self.mangas.find_one({"url": url})
            manga = Manga.dict_to_manga(results)
            return manga
        except Exception as error:
            print(error)
            return None

    def set(self, url: str, manga: Manga) -> bool:
        """Change manga with same url"""
        try:
            results = self.mangas.update_one({"url": url}, {"$set": manga.to_dict()})
            return results.matched_count == 1
        except Exception as error:
            print(error)
            return False

    def search(self, title: str) -> list[Manga]:
        """Return mangas with similar titles or alternative titles"""
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
        """Checks if manga already exists by id"""
        return self.mangas.find_one({"url": url}) != None

    def is_empty(self, origin: str = None) -> bool:
        """Return true if docs with same origin exists. If origin is None, return True if mangas 'mangas' is empty"""
        if origin == "readm":
            return self.mangas.count_documents({"origin": "readm"}) == 0
        elif origin == "manga_livre":
            return self.mangas.count_documents({"origin": "manga_livre"}) == 0

        return self.mangas.count_documents({}) == 0

    def connect(self) -> bool:
        """Connect to database and returns True if sucessful"""
        try:
            self.client: MongoClient = MongoClient(getenv("MONGO_URI"))
            self.database = self.client.get_database("manga_db")
            self.mangas = self.database.get_collection("mangas")

            return True
        except Exception as error:
            print(error)
            return False

    def close(self) -> None:
        """Close database conncetion"""
        if self.client:
            self.client.close()
