from entities.chapter import Chapter
from entities.manga import Manga
from requests import get

from .pages import get_pages

def get_chapter(manga: Manga, value: str) -> Chapter:
    """
    Returns all pages in chapter `value`.

    Arguments:
    `manga`: well... the manga. (badum tss!)
    `value`: the chapter's value.
    """
    if not check_chapter_exists(manga, value):
        msg = f"The value {value} doesn't exist in the manga: {manga.title}."
        raise Exception(msg)

    return Chapter(
        name=value, 
        pages=get_pages(manga, value), 
        id=None
    )

# It uses binary search ;)
def get_pages(manga: Manga, chapter_value: str) -> list[str]:
    low: int = 1
    high: int = 200 # I don't think there's a manga that has more than 200 pages

    title = sanitize_title(manga.title)
    initial = sanitize_initial(title)

    base_url = f'https://img.lermanga.org/{initial}/{title}/capitulo-{chapter_value}'

    # print(f'Requesting: {base_url}')

    while low <= high:
        index = (low + high) // 2
        url = f'{base_url}/{index}.jpg'
        resp = get(url)

        # print(f'{resp.status_code} |-> {url}')

        if resp.status_code != 200:
            high = index - 1
        else:
            low = index + 1

    return [f'{base_url}/{i}.jpg' for i in range(1, low)]


def sanitize_initial(title: str) -> str:
    return title[0].upper()


def sanitize_title(title: str) -> str:
    sanitized = title.lower().replace(' ', '-')
    sanitized = ''.join(char if char.isalpha() or char == '-' else '' for char in sanitized)
    return sanitized


def check_chapter_exists(manga: Manga, value: str) -> bool:
    for chapter_value in manga.chapters:
        if value == chapter_value.name:
            return True
    return False