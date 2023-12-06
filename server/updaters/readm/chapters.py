from entities.chapter import Chapter
from entities.manga import Manga
from ...api.chapters.chapter_info import add_chapters, get_chapter_names
from core.sites.readm import get_chapter
from execution.log_configs import logger


def _get_unregistered_chapters(manga: Manga) -> list[Chapter]:
    """
    Retrieves chapters of a manga that are not yet registered in the database.

    Args:
        manga (Manga): Manga info.

    Returns:
        list[str]: A list of chapters that are not registered in the database.
    """
    new_chapters: list[Chapter] = []

    chapter_names_registered = get_chapter_names(manga.id)

    for chapter in manga.chapters:
        if chapter.name not in chapter_names_registered:
            new = get_chapter(manga, chapter.name)

            if not chapter.is_empty():
                new_chapters.append(new)

    return new_chapters


def update_unregistered_chapters(manga: Manga) -> bool:
    """
    Updates chapters that are not yet registered for a given manga.

    Args:
        manga (Manga): Manga info.

    Returns:
        boolean: Return True if operation was completed successfully.
    """
    logger.info(f"({manga.origin}): updating {manga.url}")

    updated = False
    new_chapters = _get_unregistered_chapters(manga)

    if new_chapters:
        updated = add_chapters(manga.id, new_chapters)

    return updated
