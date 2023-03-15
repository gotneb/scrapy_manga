from firebase_admin.firestore import client
from core.manga import Manga

# Firestore Python docs: https://cloud.google.com/python/docs/reference/firestore/latest

class MangaDatabase:
    def __init__(self):
        try:    
            self.details_colection = client().collection("mangas").document("readm").collection("details")
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
        doc_ref = self.details_colection.add(manga_dict)
        return doc_ref

    def get_details(self, title: str):
        """returns the first document from database with same title"""
        docs = self.details_colection.where("title", "==", title).stream()
        for doc in docs:
            return doc.to_dict()
        return None

    def exists(self, title: str):
        """returns True if manga exists in database"""
        doc = self.get_details(title)
        return doc != None
    
    

db = MangaDatabase()