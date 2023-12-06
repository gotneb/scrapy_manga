from .constants import *
from entities import Manga, Chapter
from .pages import get_pages


def get_chapter(manga: Manga, value: str) -> Chapter:
    """
    Returns all pages in chapter `value`.

    Arguments:
    `manga`: well... the manga. (badum tss!)
    `value`: the chapter's value.
    """
    base_url = f"https://br.ninemanga.com/chapter/{manga.title}"
    id = None
    for chapter in manga.chapters:
        if value == chapter.name:
            id = chapter.id

    if id == None:
        err = f"There's no chapter value '{value}' in {manga.title}!"
        raise Exception(err)

    url = f"{base_url}/{id}.html"

    chapter = Chapter(name=value, pages=get_pages(url), id=id)

    return chapter


def get_all_chapters(manga: Manga) -> list[Chapter]:
    chapters = []

    for chapter in manga.chapters:
        new_chapter = get_chapter(manga, chapter.name)

        if not new_chapter.is_empty():
            chapters.append(new_chapter)

    return chapters
