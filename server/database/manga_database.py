from bson import ObjectId
from pymongo import MongoClient
from .website_update import WebsiteUpdate
from entities import Manga


class MangaDatabase:
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

    def exists(self, url: str) -> bool:
        return self.mangas.find_one({"url": url}) != None

    def add_update_info(self, update: WebsiteUpdate) -> ObjectId:
        try:
            results = self.updates.insert_one(update.to_dict())
            return results.inserted_id
        except Exception as error:
            print(error)
            return None

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
