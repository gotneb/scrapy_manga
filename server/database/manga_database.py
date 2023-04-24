from bson import ObjectId
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

    def add(self, manga: Manga) -> ObjectId:
        try:
            results = self.mangas.insert_one(manga.to_dict())
            return results.inserted_id
        except Exception as error:
            print(error)
            return None

    def add_all(self, mangas: list[Manga]) -> list[ObjectId]:
        try:
            mangas_doc = [manga.to_dict() for manga in mangas]
            results = self.mangas.insert_many(mangas_doc)
            return results.inserted_ids
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

    def remove_all(self, urls: list[str]) -> bool:
        try:
            results = self.mangas.delete_many({"url": {"$in": urls}})
            return results.deleted_count == len(urls)
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

    def search(self, search_term: str) -> list[Manga]:
        try:
            results = []
            cursor = self.mangas.find({"$text": {"$search": search_term}})
            for doc in cursor:
                results.append(Manga.dict_to_manga(doc))
            return results
        except Exception as error:
            print(error)
            return None

    def exists(self, url: str) -> bool:
        return self.mangas.find_one({"url": url}) != None

    def list_genres(self, language: str = "english") -> list[str]:
        try:
            return self.mangas.find({"language": language}).distinct("genres")
        except Exception as error:
            print(error)

    def get_mangas_by_genre(self, genre: str) -> list[Manga]:
        try:
            cursor = self.mangas.find({"genres": genre})
            results = []
            for doc in cursor:
                results.append(Manga.dict_to_manga(doc))
            return results
        except Exception as error:
            print(error)

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
