from server import MangaDatabase
from .fake_entities import *


class TestMangaDatabase:
    """Testing class MangaDatabase"""

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

    def test_search_by_title(self):
        """Testing method search (by title and alternative_title)"""
        manga = get_fake_manga()
        manga.title = "word1 word2 word3"

        self.db.add(manga)

        search_results = self.db.search("word2")
        assert search_results is not None
        assert search_results != []
        assert manga in search_results

        self.db.remove(manga.url)

    def test_search_by_author(self):
        """Testing method search (by author and artist)"""
        manga = get_fake_manga()
        manga.author = "name_author last_name_author"
        manga.artist = "name_artist last_name_artist"

        self.db.add(manga)

        search_results = self.db.search("name_author")
        assert search_results is not None
        assert search_results != []
        assert manga in search_results

        search_results = self.db.search("last_name_artist")
        assert search_results is not None
        assert search_results != []
        assert manga in search_results

        self.db.remove(manga.url)

    def test_list_genres(self):
        """Testing method search (by author and artist)"""
        manga1 = get_fake_manga()
        manga1.genres = ["action", "advanture"]
        self.db.add(manga1)

        manga2 = get_fake_manga()
        manga2.language = "portuguese"
        manga2.url = "outra_url"
        manga2.genres = ["ação", "aventura"]
        self.db.add(manga2)

        search_results = self.db.list_genres("english")
        assert set(search_results) == set(manga1.genres)

        search_results = self.db.list_genres("portuguese")
        assert set(search_results) == set(manga2.genres)

        self.db.remove(manga1.url)
        self.db.remove(manga2.url)

    def test_get_mangas_by_genre(self):
        """Testing method get_mangas_by_genre"""
        manga = get_fake_manga()
        manga.genres = ["action", "advanture"]
        self.db.add(manga)

        results = self.db.get_mangas_by_genre("action")
        assert results is not None
        assert results != []
        assert manga in results

        results = self.db.get_mangas_by_genre("advanture")
        assert results is not None
        assert results != []
        assert manga in results

        self.db.remove(manga.url)

    def test_add_and_remove_update_info(self):
        """Testing the methods add_update_info and remove_update_info"""

        update = get_fake_website_update()

        inserted_id = self.db.add_update_info(update)
        assert inserted_id is not None

        remove_res = self.db.remove_update_info(update.origin)
        assert remove_res == True

    def test_get_and_set_update_info(self):
        update = get_fake_website_update()
        self.db.add_update_info(update)

        data = self.db.get_update_info(update.origin)
        assert data is not None

        data.populars = ["outra_url"]
        res = self.db.set_update_info(data)
        assert res == True

        data = self.db.get_update_info(update.origin)
        assert data is not None
        assert data.populars == ["outra_url"]

        self.db.remove_update_info(update.origin)

    def test_info_exists(self):
        """Checks if readm and manga livre update info exists"""

        update = self.db.get_update_info("readm")
        assert update is not None
        assert update.origin == "readm"

        update = self.db.get_update_info("manga_livre")
        assert update is not None
        assert update.origin == "manga_livre"

    def test_get_populars(self):
        mangas = get_fake_manga_list(5)
        urls = [manga.url for manga in mangas]

        self.db.add_all(mangas)

        update = get_fake_website_update()
        update.populars = urls

        self.db.add_update_info(update)

        popular_mangas = self.db.get_populars(update.origin)
        assert popular_mangas is not None
        assert len(popular_mangas) == len(urls)

        self.db.remove_update_info(update.origin)
        self.db.remove_all(urls)
