from bson import ObjectId
from pymongo import MongoClient
from .website_update import WebsiteUpdate
from entities import Manga
from .database import Database


class MangaDatabase(Database):
    def __init__(self) -> None:
        self.client = None
        self.database = None
        self.mangas = None
        self.updates = None

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

    def get(self, url: str) -> dict:
        try:
            results = self.mangas.find_one({"url": url})
            return results
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

    def search(self, search_term: str) -> list[dict]:
        try:
            results = []
            cursor = self.mangas.find({"$text": {"$search": search_term}})
            for doc in cursor:
                results.append(doc)
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
            return None

    def get_mangas_by_genre(self, genre: str) -> list[dict]:
        try:
            cursor = self.mangas.find({"genres": genre})
            results = []
            for doc in cursor:
                results.append(doc)
            return results
        except Exception as error:
            print(error)
            return None

    def add_update_info(self, update: WebsiteUpdate) -> ObjectId:
        try:
            results = self.updates.insert_one(update.to_dict())
            return results.inserted_id
        except Exception as error:
            print(error)
            return None

    def remove_update_info(self, origin: str) -> bool:
        try:
            results = self.updates.delete_one({"origin": origin})
            return results.deleted_count == 1
        except Exception as error:
            print(error)
            return False

    def get_update_info(self, origin: str) -> dict:
        try:
            results = self.updates.find_one({"origin": origin})
            update = WebsiteUpdate.to_website_update(results)
            return update
        except Exception as error:
            print(error)
            return None

    def set_update_info(self, update: WebsiteUpdate) -> bool:
        try:
            results = self.updates.update_one(
                {"origin": update.origin}, {"$set": update.to_dict()}
            )
            return results.matched_count == 1
        except Exception as error:
            print(error)
            return False

    def get_populars(self, origin: str) -> list[dict]:
        try:
            results = self.updates.find_one({"origin": origin})
            urls = results["populars"]
            cursor = self.mangas.find({"origin": origin, "url": {"$in": urls}})

            mangas = []
            for doc in cursor:
                mangas.append(doc)
            return mangas
        except Exception as error:
            print(error)
            return None

    def get_latest_updates(self, origin: str) -> list[dict]:
        try:
            results = self.updates.find_one({"origin": origin})
            urls = results["latest_updates"]
            cursor = self.mangas.find({"origin": origin, "url": {"$in": urls}})

            mangas = []
            for doc in cursor:
                mangas.append(doc)
            return mangas
        except Exception as error:
            print(error)
            return None

    def is_empty(self, origin: str = None) -> bool:
        if origin == "readm":
            return self.mangas.count_documents({"origin": "readm"}) == 0
        elif origin == "manga_livre":
            return self.mangas.count_documents({"origin": "manga_livre"}) == 0

        return self.mangas.count_documents({}) == 0

    def connect(self, mongo_uri: str) -> bool:
        try:
            self.client: MongoClient = MongoClient(mongo_uri)
            self.database = self.client.get_database("manga_db")
            self.mangas = self.database.get_collection("mangas")
            self.updates = self.database.get_collection("updates")

            return True
        except Exception as error:
            print(error)
            return False

    def close(self) -> None:
        if self.client:
            self.client.close()
