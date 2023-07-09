from ..api import *

from core.sites.golden_mangas import *
from entities import Manga, ChapterInfo, Chapter, WebsiteUpdate
from .create_threads_to_update_mangas import create_threads_to_update_mangas
from .utils import get_chapters_not_registered, filter_empty_chapters
from execution.log_configs import logger


origin = "golden_mangas"
language = "portuguese"


def update_mangas(number_of_works: int, exec_all: bool = False):
    """Get the manga urls and update the database."""

    try:
        # Update site information in database
        latest_updated_urls = get_latest_updated_urls()
        popular_urls = get_popular_urls()

        registed_info = get_origin_info(origin)

        # define if process all urls
        if (not registed_info) or exec_all:
            urls_for_update = get_all_urls()
        else:
            urls_for_update = latest_updated_urls

        # create threads
        create_threads_to_update_mangas(urls_for_update, feat, number_of_works)

        # update informations about mangas in the api
        info = WebsiteUpdate(
            origin=origin,
            language=language,
            populars=popular_urls,
            latest_updates=latest_updated_urls,
        )

        if registed_info:
            # Keep info about popular mangas if new list is empty
            if len(info.populars) == 0:
                info.populars = registed_info.populars

            # Keep info about popular mangas if new list is empty
            if len(info.latest_updates) == 0:
                info.latest_updates = registed_info.latest_updates

        update_info(info)

    except Exception as error:
        logger.critical(
            f"({origin}) on update mangas.",
            exc_info=True,
        )


def feat(manga_url: str):
    """Check if manga is in the database, saving the manga or updating chapters."""

    logger.info(f"({origin}): processing {manga_url}")

    try:
        manga_id = manga_exists(manga_url)

        if manga_id:
            update(manga_id, manga_url)
        else:
            save(manga_url)

    except Exception as error:
        logger.error(
            f"({origin}): error in the processing of {manga_url}",
            exc_info=True,
        )


def update(manga_id: str, manga_url):
    """Checks for missing chapters and updates them."""
    manga = get_manga_without_chapter_pages(manga_url)
    chapter_names_registered = get_chapter_names(manga_id)

    new_chapters: list[Chapter] = []

    for info in get_chapters_not_registered(
        manga.chapters_info, chapter_names_registered
    ):
        chapter = get_chapter(manga_url, info)
        new_chapters.append(chapter)

    new_chapters = filter_empty_chapters(new_chapters)

    if len(new_chapters) > 0:
        add_chapters(manga_id, new_chapters)


def save(manga_url: str):
    """Save a new manga in the database."""
    manga = get_manga_with_chapter_pages(manga_url)
    manga.chapters = filter_empty_chapters(manga.chapters)

    # if manga contain chapters
    if len(manga.chapters) > 0:
        add_manga(manga)


def get_all_urls():
    logger.info(f"({origin}): downloading all mangas URLs.")
    urls = []

    for letter in [chr(i) for i in range(97, 123)]:
        try:
            letter_urls = get_all_start_with(letter=letter)
            urls = urls + letter_urls
        except Exception as error:
            logger.critical(
                f"({origin}) error getting all URLs.",
                exc_info=True,
            )

    return urls


def get_latest_updated_urls():
    logger.info(f"({origin}): downloading updated mangas URLs.")
    urls = []

    try:
        urls = urls + get_latest_updates(limit=400)
    except Exception as error:
        logger.critical(
            f"({origin}) error getting latest updated URLs.",
            exc_info=True,
        )

    return urls


def get_popular_urls():
    logger.info(f"({origin}): downloading popular mangas URLs.")
    urls = []

    try:
        urls = urls + get_populars()
    except Exception as error:
        logger.critical(
            f"({origin}) error getting populars URLs.",
            exc_info=True,
        )

    return urls


def get_manga_without_chapter_pages(manga_url: str) -> Manga:
    return manga_detail(manga_url, False)


def get_manga_with_chapter_pages(manga_url: str) -> Manga:
    # download manga info
    manga = manga_detail(manga_url, False)
    manga.chapters = []

    # dowload chapter pages
    for info in manga.chapters_info:
        chapter = get_chapter(manga_url, info)

        # if chapter contains pages
        if len(chapter.pages) > 0:
            manga.chapters.append(chapter)

    return manga


def get_chapter(manga_url: str, info: ChapterInfo) -> Chapter:
    cp_url = f"{manga_url}/{info.name}"
    pages = get_pages(cp_url)

    return Chapter(name=info.name, pages=pages)
