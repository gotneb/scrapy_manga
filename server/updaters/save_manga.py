from entities.manga import Manga
from ..api.manga.manga_info import add_manga
from execution.log_configs import logger


def save_new_manga(manga: Manga) -> str:
    """
    Saves a new manga to the database.

    Args:
        manga (Manga): Manga info.

    Returns:
        str: Manga ID inserted.
    """
    logger.info(f"({manga.origin}): saving {manga.url}")

    inserted_id = None

    # if manga contain chapters
    if not manga.is_empty():
        inserted_id = add_manga(manga)

    return inserted_id
