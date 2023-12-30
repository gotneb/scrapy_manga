from entities.chapter import Chapter
from entities.manga import Manga

from .pages import get_pages

def get_chapter(manga: Manga, value: str) -> Chapter:
    """
    Returns all pages in chapter `value`.

    Arguments:
    `manga`: well... the manga. (badum tss!)
    `value`: the chapter's value.
    """
    title = sanitize_title(manga.title)
    url = f'https://lermanga.org/capitulos/{title}-capitulo-{value}/'

    print(url)
    
    if not check_chapter_exists(manga, value):
        msg = f"The value {value} doesn't exist in the manga: {manga.title}."
        raise Exception(msg)

    return Chapter(
        name=value, 
        pages=get_pages(url), 
        id=None
    )


def sanitize_title(title: str) -> str:
    return  title              \
            .lower()           \
            .replace(',', '')  \
            .replace(' ', '-') \
            .replace(':', '') \


def check_chapter_exists(manga: Manga, value: str) -> bool:
    for chapter_value in manga.chapters:
        if value == chapter_value.name:
            return True
    return False