from firebase_admin.firestore import client
from core.manga import Manga
from core.sites.readm import manga_detail, get_pages

# Firestore Python docs: https://cloud.google.com/python/docs/reference/firestore/latest

db = client();
details_colection = db.collection("mangas").document("readm").collection("details")

def add_manga_details(manga: Manga):
    """
    Add a new manga details to the database
    Returns:
        A reference to the created document
    """
    manga_dict = manga.to_dict()
    if manga_exists(manga_dict['title']):
        return None
    doc_ref = details_colection.add(manga_dict)
    return doc_ref

def get_manga_details(title: str):
    """returns the first document from database with same title"""
    docs = details_colection.where("title", "==", title).stream()
    for doc in docs:
        return doc.to_dict()
    return None

def manga_exists(title: str):
    """returns True if manga exists in database"""
    doc = get_manga_details(title)
    return doc != None