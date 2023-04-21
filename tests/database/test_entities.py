from server import Manga
from .fake_entities import get_fake_manga


def test_manga_entitie():
    # Testing class manga
    manga = get_fake_manga()
    assert manga is not None

    # testing method to_dict()

    manga_dict = manga.to_dict()

    assert manga_dict is not None
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

    # testing method Manga.dict_to_manga()

    dict_to_manga = Manga.dict_to_manga(manga_dict)

    assert dict_to_manga is not None
    assert manga_dict["title"] == dict_to_manga.title
    assert manga_dict["alternative_title"] == dict_to_manga.alternative_title
    assert manga_dict["author"] == dict_to_manga.author
    assert manga_dict["artist"] == dict_to_manga.artist
    assert manga_dict["status"] == dict_to_manga.status
    assert manga_dict["url"] == dict_to_manga.url
    assert manga_dict["origin"] == dict_to_manga.origin
    assert manga_dict["language"] == dict_to_manga.language
    assert manga_dict["thumbnail"] == dict_to_manga.thumbnail
    assert manga_dict["genres"] == dict_to_manga.genres
    assert manga_dict["summary"] == dict_to_manga.summary
    assert manga_dict["chapters"] == dict_to_manga.chapters
