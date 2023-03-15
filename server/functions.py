from firebase_admin.firestore import client
from core.manga import Manga
from core.sites.readm import manga_detail, get_pages

# Firestore Python docs: https://cloud.google.com/python/docs/reference/firestore/latest

db = client();
details_colection = db.collection("mangas").document("readm").collection("details")

def get_manga_details(title: str):
    """returns the first document from database with same title"""
    docs = details_colection.where("title", "==", title).stream()
    for doc in docs:
        return doc.to_dict()
    return None

def manga_exists(title: str):
    doc = get_manga_details(title)
    return doc != None