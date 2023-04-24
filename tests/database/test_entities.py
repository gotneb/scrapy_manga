from server.database.entities import *
from .fake_entities import get_fake_manga, get_fake_website_update
from dataclasses import dataclass


@dataclass
class FakeEntity(Entity):
    attr1: str
    attr2: int


class TestEntity:
    """Testing class Entity"""

    def test_to_dict(self):
        fake_entity = FakeEntity("any text", 10)
        fake_entity_dict = fake_entity.to_dict()

        assert fake_entity_dict["attr1"] == fake_entity.attr1
        assert fake_entity_dict["attr2"] == fake_entity.attr2


class TestManga:
    """Testing class Manga"""

    def test_to_manga(self):
        """testing method Manga.to_manga()"""
        manga_dict = get_fake_manga().to_dict()
        manga = Manga.to_manga(manga_dict)

        assert manga is not None
        assert manga_dict["title"] == manga.title
        assert manga_dict["alternative_title"] == manga.alternative_title
        assert manga_dict["author"] == manga.author
        assert manga_dict["artist"] == manga.artist
        assert manga_dict["status"] == manga.status
        assert manga_dict["url"] == manga.url
        assert manga_dict["origin"] == manga.origin
        assert manga_dict["language"] == manga.language
        assert manga_dict["thumbnail"] == manga.thumbnail
        assert manga_dict["genres"] == manga.genres
        assert manga_dict["summary"] == manga.summary
        assert manga_dict["chapters"] == manga.chapters


class TestWebsiteUpdate:
    """Testing class WebsiteUpdate"""

    def test_to_update(self):
        """Testing method to_update"""
        update_dict = get_fake_website_update().to_dict()
        update = WebsiteUpdate.to_website_update(update_dict)

        assert update is not None
        assert update.origin == update_dict["origin"]
        assert update.populars == update_dict["populars"]
        assert update.latest_updates == update_dict["latest_updates"]
