from firebase_admin.firestore import client
from core.manga import Manga
from .entities import ChapterEntity, MangaDetailsEntity
from operator import itemgetter

# Firestore Python docs: https://cloud.google.com/python/docs/reference/firestore/latest

class MangaDatabase:
    def __init__(self):
        try:    
            self.db = client()
            self.details_collection = self.db.collection("details")
            self.chapters_collection = self.db.collection("chapters")
        except:
            Exception("Database connection failed!")
    
    def add_details(self, manga: MangaDetailsEntity) -> str:
        """
        Add a new manga details to the database
        Returns:
            A reference to the created document
        """
        manga_dict = manga.to_dict()
        if self.manga_exists_by_title(manga_dict['title']):
            return None
        _, doc_ref = self.details_collection.add(manga_dict)
        return doc_ref.id
    
    def remove_details(self, id: str) -> bool:
        """Remove a manga by id"""
        try:
            self.details_collection.document(id).delete()
            return True
        except:
            return False
    
    def set_details(self, id: str, manga: MangaDetailsEntity) -> bool:
        """Update manga details by id"""
        try:
            self.details_collection.document(id).set(manga.to_dict())
            return True
        except:
            return False

    def get_details_by_title(self, title: str) -> dict:
        """returns the first document from database with same title"""
        docs = self.details_collection.where("title", "==", title).stream()
        for doc in docs:
            manga_details = doc.to_dict()
            manga_details['id'] = doc.id
            return manga_details
        return None
    
    def get_details_by_id(self, id: str) -> dict:
        """returns the element with same id"""
        doc = self.details_collection.document(id).get()
        if doc:
            manga_details = doc.to_dict()
            manga_details['id'] = doc.id
            return manga_details
        else:
            return None

    def manga_exists_by_title(self, title: str) -> bool:
        """returns True if manga exists in database"""
        doc = self.get_details_by_title(title)
        return doc != None
    
    def manga_exists_by_id(self, id: str) -> bool:
        """returns True if manga exists in database"""
        doc = self.get_details_by_id(id)
        return doc != None
    
    def add_chapter(self, chapter: ChapterEntity) -> str:
        """Add new chapter in database"""
        if self.manga_exists_by_id(chapter.manga_id):
            chapter_dict = chapter.to_dict()
            _, doc_ref = self.chapters_collection.add(chapter_dict)
            return doc_ref.id
        else:
            return None
    
    def get_chapter(self, manga_id: str, chapter_num: str) -> tuple[str, dict]:
        """Return the first chapter with same manga_id and chapter_sum"""
        docs = self.chapters_collection \
            .where("manga_id", "==", manga_id) \
                .where("chapter_num", "==", chapter_num) \
                    .stream()
        
        for doc in docs:
            return doc.id, doc.to_dict()
        return None
    
    def set_chapter(self, id: str, chapter: ChapterEntity) -> bool:
        """Update chapter by id"""
        try:
            if self.manga_exists_by_id(id):
                self.chapters_collection.document(id).set(chapter.to_dict())
            return True
        except:
            return False
        
    def remove_chapter(self, id: str) -> bool:
        """Remove a chapter by id"""
        try:
            self.chapters_collection.document(id).delete()
            return True
        except:
            return False
    
    def search_details(self, queryText: str) -> list[dict]:
        """Returns a list with documents whose title contains the queryText"""
        docs = self.details_collection.where("title", ">=", queryText).where("title", "<=", queryText + "\uf8ff").get()
        results: list[dict] = []

        for doc in docs:
            manga_details = doc.to_dict()
            manga_details['id'] = doc.id
            results.append(manga_details)
        
        return results
            
        
db = MangaDatabase()