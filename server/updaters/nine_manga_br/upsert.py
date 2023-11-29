from ...api.manga.manga_info import manga_exists, add_manga
from ...api.chapters.chapter_info import add_chapters

from .constants import origin
from execution.log_configs import logger

from .manga_info import get_manga, get_unregistered_chapters


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
            ok = _update_unregistered_chapters(manga_id, manga_url)
        else:
            ok = _save_new_manga(manga_url) != None

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


def _update_unregistered_chapters(manga_id: str, manga_url: str) -> bool:
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


def _save_new_manga(manga_url: str) -> str:
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
