from entities.chapter_info import ChapterInfo


def get_chapters_not_registered(
    chapters_info: list[ChapterInfo], chapter_names_registered: list[str]
) -> list[ChapterInfo]:
    """Returns chapter info not registed in database"""
    informations = []

    for info in chapters_info:
        if not info.name in chapter_names_registered:
            informations.append(info)
    return informations
