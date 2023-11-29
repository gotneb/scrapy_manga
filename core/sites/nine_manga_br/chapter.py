from .constants import *
from entities import Manga
from .pages import get_pages


def get_chapter(manga: Manga, value: str) -> list[str]:
    '''
    Returns all pages in chapter `value`.

    Arguments:
    `manga`: well... the manga. (badum tss!)
    `value`: the chapter's value.
    '''
    if type(value) is not str:
        err = f'The value `{value}` {type(value)} is not the type of str!'
        raise Exception(err)
    
    base_url = f'https://br.ninemanga.com/chapter/{manga.title}'
    id = None
    for info in manga.chapters_info:
        if value == info.name:
            id = info.id

    if id == None:
        err = f"There's no chapter value '{value}' in {manga.title}!"
        raise Exception(err)

    url = f'{base_url}/{id}.html'
    return get_pages(url)
