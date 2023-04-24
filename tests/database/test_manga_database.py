from server import MangaDatabase
from .fake_entities import *


def test_connection():
    """Testing database connection"""
    db = MangaDatabase()
    connection_results = db.connect()

    assert connection_results == True

    db.close()


def test_add_all_and_remove_all():
    db = MangaDatabase()
    db.connect()
    mangas = get_fake_manga_list()

    add_res = db.add_all(mangas)
    assert add_res is not None

    urls = [manga.url for manga in mangas]
    remove_res = db.remove_all(urls)
    assert remove_res == True

    db.close()


def test_integrated_insertion_and_deletion():
    """Testing methods add, remove and exists"""
    db = MangaDatabase()
    db.connect()

    # insertion test
    manga = get_fake_manga()
    inserted_id = db.add(manga)
    assert inserted_id is not None

    inserted_id = db.add(manga)
    assert inserted_id is None

    # test of method exist
    exists = db.exists(manga.url)
    assert exists == True

    # deletion test
    remove_results = db.remove(manga.url)
    assert remove_results == True

    remove_results = db.remove(manga.url)
    assert remove_results == False

    db.close()


def test_get_and_set():
    """Testing methods get and set"""

    db = MangaDatabase()
    db.connect()

    manga = get_fake_manga()
    db.add(manga)

    # testing method test
    recoved_manga = db.get(manga.url)
    assert recoved_manga.title == manga.title

    # testing method set
    new_title = "other_title"
    recoved_manga.title = new_title
    set_results = db.set(manga.url, recoved_manga)
    assert set_results == True

    recoved_manga = db.get(manga.url)
    assert recoved_manga.title == new_title

    db.remove(manga.url)

    db.close()


def test_search():
    """Testing method search"""
    manga = get_fake_manga()
    manga.title = "word1 word2 word3"
    manga.author = "nome_author sobrenome_author"
    manga.artist = "nome_artist sobrenome_artist"

    db = MangaDatabase()
    db.connect()

    db.add(manga)

    # testing method search
    search_results = db.search("word2")
    assert search_results is not None
    assert search_results != []
    assert manga in search_results

    # testing method search
    search_results = db.search("nome_author")
    assert search_results is not None
    assert search_results != []
    assert manga in search_results

    # testing method search
    search_results = db.search("sobrenome_artist")
    assert search_results is not None
    assert search_results != []
    assert manga in search_results

    db.remove(manga.url)
    db.close()
