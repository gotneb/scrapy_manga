import traceback
from ..api import *
import re

from core.sites.manga_livre import *
from entities import Manga, ChapterInfo, Chapter, WebsiteUpdate
from .create_threads_to_update_mangas import create_threads_to_update_mangas
from .utils import get_chapters_not_registered
from execution.log_configs import logger


origin = "manga_livre"
language = "portuguese"


def update_mangas(number_of_works: int, exec_all: bool = False):
    """Get the manga urls and update the database."""

    # Update site information in database
    latest_updated_urls = get_latest_updated_urls()
    popular_urls = get_popular_urls()

    info = WebsiteUpdate(
        origin=origin,
        language=language,
        populars=popular_urls,
        latest_updates=latest_updated_urls,
    )

    site_already_registered = origin_exists(info.origin)

    if site_already_registered:
        update_info(info)
    else:
        add_info(info)

    # define if process all urls
    if (not site_already_registered) or exec_all:
        urls_for_update = get_all_urls()
    else:
        urls_for_update = latest_updated_urls

    # create threads
    create_threads_to_update_mangas(urls_for_update, feat, number_of_works)


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
            f"({origin}): failure {manga_url}\n   -> error: {error.args[0]} \n\n {error.with_traceback()} \n\n"
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

    if len(new_chapters) > 0:
        add_chapters(manga_id, new_chapters)


def save(manga_url: str):
    """Save a new manga in the database."""
    manga = get_manga_with_chapter_pages(manga_url)
    add_manga(manga)


def get_all_urls():
    logger.info(f"({origin}): downloading all mangas URLs.")
    urls = []

    for letter in [chr(i) for i in range(97, 123)]:
        try:
            letter_urls = get_all_start_with(letter=letter)
            urls = urls + letter_urls
        except Exception:
            logger.error(traceback.format_exc())

    return urls


def get_latest_updated_urls():
    logger.info(f"({origin}): downloading updated mangas URLs.")
    urls = []

    try:
        urls = urls + get_latest_updates(limit=400)
    except Exception:
        logger.error(traceback.format_exc())

    return urls


def get_popular_urls():
    logger.info(f"({origin}): downloading popular mangas URLs.")
    urls = []

    try:
        urls = urls + get_populars()
    except Exception:
        logger.error(traceback.format_exc())

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
    pattern = r"manga/([^/]+)"
    slug = re.search(pattern=pattern, string=manga_url).group(1)

    cp_url = f" https://mangalivre.net/ler/{slug}/online/{info.id}/{info.name}"
    pages = get_pages(cp_url)

    return Chapter(name=info.name, pages=pages)
