from firebase_admin.firestore import client
from core.manga import Manga

# Firestore Python docs: https://cloud.google.com/python/docs/reference/firestore/latest


def add_manga(manga: Manga):
    """Add manga to online database"""
    # Reference to mangas collection
    mangas_ref = client()     \
    .collection('readm')      \
    .document('manga_details')\
    .collection('mangas')

    doc_ref = mangas_ref.add(manga.to_dict())
