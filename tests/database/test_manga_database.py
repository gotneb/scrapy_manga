from server import MangaDatabase
from .fake_entities import *


class TestMangaDatabase:
    db = MangaDatabase()

    def test_connection(self):
        """Testing database connection"""
        connection_results = self.db.connect()
        assert connection_results == True

    def test_integrated_insertion_and_deletion(self):
        """Testing methods add, remove and exists"""

        # insertion test
        manga = get_fake_manga()
        inserted_id = self.db.add(manga)
        assert inserted_id is not None

        inserted_id = self.db.add(manga)
        assert inserted_id is None

        # test of method exist
        exists = self.db.exists(manga.url)
        assert exists == True

        # deletion test
        remove_results = self.db.remove(manga.url)
        assert remove_results == True

        remove_results = self.db.remove(manga.url)
        assert remove_results == False

    def test_add_all_and_remove_all(self):
        """Testing methods add_all and remove_all"""
        mangas = get_fake_manga_list()

        add_res = self.db.add_all(mangas)
        assert add_res is not None

        urls = [manga.url for manga in mangas]
        remove_res = self.db.remove_all(urls)
        assert remove_res == True

    def test_get_and_set(self):
        """Testing methods get and set"""

        manga = get_fake_manga()
        self.db.add(manga)

        # testing method test
        recoved_manga = self.db.get(manga.url)
        assert recoved_manga.title == manga.title

        # testing method set
        new_title = "other_title"
        recoved_manga.title = new_title
        set_results = self.db.set(manga.url, recoved_manga)
        assert set_results == True

        recoved_manga = self.db.get(manga.url)
        assert recoved_manga.title == new_title

        self.db.remove(manga.url)

    def test_search(self):
        """Testing method search"""
        manga = get_fake_manga()
        manga.title = "word1 word2 word3"
        manga.author = "nome_author sobrenome_author"
        manga.artist = "nome_artist sobrenome_artist"

        self.db.add(manga)

        # testing method search
        search_results = self.db.search("word2")
        assert search_results is not None
        assert search_results != []
        assert manga in search_results

        # testing method search
        search_results = self.db.search("nome_author")
        assert search_results is not None
        assert search_results != []
        assert manga in search_results

        # testing method search
        search_results = self.db.search("sobrenome_artist")
        assert search_results is not None
        assert search_results != []
        assert manga in search_results

        self.db.remove(manga.url)
