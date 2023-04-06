from pymongo import MongoClient
from bson.objectid import ObjectId
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
                raise Exception(
                    f'Document with title "{manga.title} (origin: {manga.origin})" already exists.'
                )

            results = self.collection.insert_one(manga.to_dict())
            return results.inserted_id
        except Exception as error:
            print(error)
            return None

    def remove(self, id: str) -> bool:
        """Delete document with same id in database"""
        try:
            results = self.collection.delete_one({"_id": ObjectId(id)})
            return results.deleted_count == 1
        except Exception as error:
            print(error)
            return False

    def get(self, id: str) -> Manga:
        """Returns document with same id"""
        try:
            results = self.collection.find_one({"_id": ObjectId(id)})
            return Manga.dict_to_manga(results)
        except Exception as error:
            print(error)
            return None

    def set(self, id: str, manga: Manga) -> bool:
        """Change manga with same id"""
        try:
            results = self.collection.update_one(
                {"_id": ObjectId(id)}, {"$set": manga.to_dict()}
            )
            return results.matched_count == 1
        except Exception as error:
            print(error)
            return False

    def get_by_url(self, url: str) -> Manga:
        """Returns document with same url"""
        try:
            results = self.collection.find_one({"url": url})
            manga = Manga.dict_to_manga(results)
            return manga
        except Exception as error:
            print(error)
            return None

    def set_by_url(self, url: str, manga: Manga) -> bool:
        """Change manga with same url"""
        try:
            results = self.collection.update_one(
                {"url": url}, {"$set": manga.to_dict()}
            )
            return results.matched_count == 1
        except Exception as error:
            print(error)
            return False

    def search_by_title(self, title: str) -> list[Manga]:
        """Return mangas with similar titles or alternative titles"""
        try:
            results = []
            cursor = self.collection.find({"$text": {"$search": title}})
            for doc in cursor:
                results.append(Manga.dict_to_manga(doc))
            return results
        except Exception as error:
            print(error)
            return None

    def exists_by_manga(self, manga: Manga) -> bool:
        """Checks if manga already exists by manga object"""
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

    def exists_by_id(self, id: str) -> bool:
        """Checks if manga already exists by id"""
        return self.collection.find_one({"_id": ObjectId(id)}) != None

    def exists_by_url(self, url: str) -> bool:
        """Checks if manga already exists by id"""
        return self.collection.find_one({"url": url}) != None

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

    def is_empty(self, origin: str = None) -> bool:
        """Return true if docs with same origin exists. If origin is None, return True if collection 'mangas' is empty"""
        if origin == "readm":
            return self.collection.count_documents({"origin": "readm"}) == 0
        elif origin == "manga_livre":
            return self.collection.count_documents({"origin": "manga_livre"}) == 0

        return self.collection.count_documents({}) == 0

    def close(self) -> None:
        """Close database conncetion"""
        if self.client:
            self.client.close()
