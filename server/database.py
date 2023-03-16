from firebase_admin.firestore import client
from core.manga import Manga

# Firestore Python docs: https://cloud.google.com/python/docs/reference/firestore/latest

class MangaDatabase:
    def __init__(self):
        try:    
            self.db = client().collection("mangas").document("readm")
            self.details_collection = self.db.collection("details")
            self.pages_collection = self.db.collection("pages")
        except:
            Exception("Database connection failed!")
    
    def add_details(self, manga: Manga):
        """
        Add a new manga details to the database
        Returns:
            A reference to the created document
        """
        manga_dict = manga.to_dict()
        if self.exists(manga_dict['title']):
            return None
        _, doc_ref = self.details_collection.add(manga_dict)
        return doc_ref.id
    
    def remove_details(self, id: str):
        """Remove a manga by id"""
        try:
            self.details_collection.document(id).delete()
            return True
        except:
            return False
    
    def set_details(self, id: str, manga: Manga):
        """Update manga details by id"""
        try:
            self.details_collection.document(id).set(manga.to_dict())
            return True
        except:
            return False

    def get_details(self, title: str):
        """returns the first document from database with same title"""
        docs = self.details_collection.where("title", "==", title).stream()
        for doc in docs:
            return doc.to_dict(), doc.id
        return None

    def exists(self, title: str):
        """returns True if manga exists in database"""
        doc = self.get_details(title)
        return doc != None
    
    

db = MangaDatabase()