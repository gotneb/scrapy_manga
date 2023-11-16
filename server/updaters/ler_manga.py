from ..api import *
from core.sites.ler_manga import *
from entities import Manga, Chapter, WebsiteUpdate
from .create_threads_to_update_mangas import create_threads_to_update_mangas
from execution.log_configs import logger

import re

origin = "ler_manga"
language = "portuguese"


def update_mangas_from_websites(number_of_works: int, exec_all: bool = False):
    """
    Updates manga from website.

    Args:
        number_of_works (int): Number of threads used for accessing the website.
        exec_all (bool): If True, updates all mangas from the website.

    Returns:
        None
    """

    logger.info(f"Updating mangas from {origin}.")

    try:
        # Update site information in database
        popular_urls = get_most_popular_manga_urls()
        registed_info = get_origin_info(origin)

        # define if process all urls
        if (not registed_info) or exec_all:
            urls_for_update = get_all_urls_in_alphabetic_order()
        else:
            urls_for_update = get_latest_updated_manga_urls()

        # create threads
        create_threads_to_update_mangas(urls_for_update, upsert_manga, number_of_works)

        # update informations about mangas in the api
        if popular_urls:
            info = WebsiteUpdate(origin, popular_urls, language)
            update_info(info)

    except Exception as error:
        logger.critical(
            f"({origin}) on update mangas.",
            exc_info=True,
        )


def upsert_manga(manga_url: str) -> bool:
    """
    If the manga url is already registered, it saves the manga in the API.
    Otherwise, it updates its chapters.

    Args:
        manga_url (str): The URL of the manga to be checked and saved or updated.

    Returns:
        boolean: Return True if operation was completed successfully.
    """
    ok = False

    try:
        manga_id = manga_exists(manga_url)

        if manga_id:
            ok = update_unregistered_chapters(manga_id, manga_url)
        else:
            ok = save_new_manga(manga_url) != None

        if ok:
            logger.info(f"({origin}): operation completed successfully on {manga_url}")
        else:
            logger.warning(f"({origin}): operation failed on {manga_url}")
    except Exception as error:
        logger.error(
            f"({origin}): error in the processing of {manga_url}",
            exc_info=True,
        )

    return ok


def update_unregistered_chapters(manga_id: str, manga_url: str) -> bool:
    """
    Updates chapters that are not yet registered for a given manga.

    Args:
        manga_id (str): The ID of the manga.
        manga_url (str): The URL of the manga to be checked and updated.

    Returns:
        boolean: Return True if operation was completed successfully.
    """
    logger.info(f"({origin}): updating {manga_url}")

    updated = False
    new_chapters = get_unregistered_chapters(manga_id, manga_url)

    if new_chapters:
        updated = add_chapters(manga_id, new_chapters)

    return updated


def save_new_manga(manga_url: str) -> str:
    """
    Saves a new manga to the database.

    Args:
        manga_url (str): The URL of the manga to be added to the database.

    Returns:
        str: Manga ID inserted.
    """
    logger.info(f"({origin}): saving {manga_url}")

    inserted_id = None
    manga = get_manga(manga_url)

    # if manga contain chapters
    if not manga.is_empty():
        inserted_id = add_manga(manga)

    return inserted_id


def get_all_urls_in_alphabetic_order() -> list[str]:
    """
    Retrieves all URLs from the website and returns them in alphabetical order.

    Returns:
        list[str]: A list of URLs sorted in alphabetical order.
    """
    logger.info(f"({origin}): downloading all mangas URLs.")
    urls = []

    for letter in [chr(i) for i in range(97, 123)]:
        try:
            urls = urls + get_all_start_with(letter=letter)
        except Exception as error:
            logger.critical(
                f"({origin}) error getting all URLs (letter={letter}).",
                exc_info=True,
            )

    return urls


def get_latest_updated_manga_urls() -> list[dict]:
    """
    Retrieves URLs of mangas that were most recently updated on the website.

    Returns:
        list[str]: A list of URLs of the latest updated mangas.
    """
    logger.info(f"({origin}): downloading updated mangas URLs.")
    manga_urls = []

    try:
        # get manga urls from chapters updates
        chapters_urls = get_latest_updates(limit=400)
        urls = [extract_manga_url(cp_url) for cp_url in chapters_urls]

        # remove repeated URLs
        for url in urls:
            if url not in manga_urls:
                manga_urls.append(url)

        manga_urls.reverse()
    except Exception as error:
        logger.critical(
            f"({origin}) error getting latest updated URLs.",
            exc_info=True,
        )

    return manga_urls


def extract_manga_url(chapter_url: str) -> str:
    slug_pattern = r"capitulos/(.*?)-capitulo-"

    search_manga_slug = re.search(slug_pattern, chapter_url)

    if search_manga_slug:
        manga_slug = search_manga_slug.group(1)
        manga_url = f"https://lermanga.org/mangas/{manga_slug}/"

        return manga_url

    return None


def get_most_popular_manga_urls() -> list[str]:
    """
    Retrieves URLs of the most popular mangas from the website.

    Returns:
        list[str]: A list of URLs of the most popular mangas.
    """
    logger.info(f"({origin}): downloading popular mangas URLs.")
    urls = []

    try:
        urls = get_populars()
    except Exception as error:
        logger.critical(
            f"({origin}) error getting populars URLs.",
            exc_info=True,
        )

    return urls


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
            chapter.pages = get_chapter_pages(manga_url, chapter)

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
        chapter.pages = get_chapter_pages(manga_url, chapter)

    manga.filter_empty_chapters()

    return manga


def get_chapter_pages(manga_url: str, chapter: Chapter) -> list[str]:
    """
    Retrieves URLs of the chapter pages for a specific chapter of a manga.

    Args:
        manga_url (str): The URL of the manga.
        chapter (Chapter): The chapter info for which pages should be retrieved.

    Returns:
        list[str]: A list of URLs of the chapter pages.
    """
    pages = []

    pattern = r"mangas/(.*?)/"
    search_string_results = re.search(pattern, manga_url)

    if search_string_results:
        manga_slug = search_string_results.group(1)
        cp_url = f"https://lermanga.org/capitulos/{manga_slug}-capitulo-{chapter.name}/"
        pages = get_pages(cp_url)

    return pages
