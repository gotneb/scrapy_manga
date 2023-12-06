from ...api.manga.manga_info import manga_exists
from .chapters import update_unregistered_chapters
from ..save_manga import save_new_manga

from .constants import origin
from core.sites.readm import manga_detail, get_all_chapters

from execution.log_configs import logger


def upsert_manga(manga_url: str) -> bool:
    """
    If the manga url is already registered, it saves the manga in the API.
    Otherwise, it updates its chapters.

    Args:
        manga_url (str): The URL of the manga to be checked and saved or updated.

    Returns:
        boolean: Return True if operation was completed successfully.
    """
    results = False

    try:
        manga = manga_detail(manga_url)
        manga_id = manga_exists(manga.url)

        if manga_id:
            manga.id = manga_id
            results = update_unregistered_chapters(manga)

            if results:
                logger.info(
                    f"({manga.origin}): manga updated successfully (id: {manga.id}, url: {manga.url})"
                )
            else:
                logger.warning(
                    f"({manga.origin}): manga update falided (id: {manga.id}, url: {manga.url})"
                )

        else:
            manga.chapters = get_all_chapters(manga)
            insertd_id = save_new_manga(manga) != None

            if insertd_id:
                results = True
                manga.id = insertd_id
                logger.info(
                    f"({manga.origin}): manga inserted successfully (id: {manga.id}, url: {manga.url})"
                )
            else:
                logger.warning(
                    f"({manga.origin}): manga not inserted (url: {manga.url})"
                )

    except Exception as error:
        logger.error(
            f"({origin}): error in the processing of {manga_url}",
            exc_info=True,
        )

    return results
