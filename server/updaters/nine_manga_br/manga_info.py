from ...api.chapters.chapter_info import get_chapter_names

from core.sites.nine_manga_br.detail import manga_detail
from core.sites.nine_manga_br.chapter import get_chapter

from entities import Manga, Chapter


def get_unregistered_chapters(manga_id: str, manga_url: str) -> list[Chapter]:
    """
    Retrieves chapters of a manga that are not yet registered in the database.

    Args:
        manga_id (str): The ID of the manga.
        manga_url (str): The URL of the manga.

    Returns:
        list[str]: A list of chapters that are not registered in the database.
    """
    new_chapters: list[Chapter] = []

    manga = get_manga_without_chapter_pages(manga_url)
    chapter_names_registered = get_chapter_names(manga_id)

    for chapter in manga.chapters:
        if chapter.name not in chapter_names_registered:
            chapter.pages = get_chapter(manga, chapter.name)

            if not chapter.is_empty():
                new_chapters.append(chapter)

    return new_chapters


def get_manga_without_chapter_pages(manga_url: str) -> Manga:
    """
    Retrieves information about a manga, excluding its chapter pages.

    Args:
        manga_url (str): The URL of the manga.

    Returns:
        Manga: A manga object without chapter pages.
    """
    return manga_detail(manga_url)


def get_manga(manga_url: str) -> Manga:
    """
    Retrieves information about a manga, including its chapter pages.

    Args:
        manga_url (str): The URL of the manga.

    Returns:
        Manga: A manga object with chapter pages included.
    """

    # download manga info
    manga = manga_detail(manga_url)

    # dowload chapter pages
    for chapter in manga.chapters:
        chapter.pages = get_chapter(manga, chapter.name)

    manga.filter_empty_chapters()

    return manga
