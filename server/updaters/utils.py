from entities.chapter_info import ChapterInfo
from entities.chapter import Chapter


def get_chapters_not_registered(
    chapters_info: list[ChapterInfo], chapter_names_registered: list[str]
) -> list[ChapterInfo]:
    """Returns chapter info not registed in database"""
    informations = []

    for info in chapters_info:
        if not info.name in chapter_names_registered:
            informations.append(info)
    return informations


def filter_empty_chapters(chapters: list[Chapter]) -> list[Chapter]:
    """Filter chapters without pages."""
    results = filter(lambda chapter: not chapter_is_empty(chapter), chapters)
    chapters_non_empty = list(results)
    return chapters_non_empty


def chapter_is_empty(chapter: Chapter) -> bool:
    """Returns True if chapter has no pages"""
    return len(chapter.pages) == 0
