from .constants import *
from entities import Manga
from .pages import get_pages


def get_chapter(manga: Manga, value: str) -> list[str]:
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
    print(f"Requesting to: {url}")
    return get_pages(url)