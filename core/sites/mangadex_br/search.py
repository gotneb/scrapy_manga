from requests import get
from core.sites.mangadex_br.manga import get_manga

from entities.manga import Manga
from .constants import base_url

def search(title: str) -> list[Manga]:
    r = get(
        f"{base_url}/manga",
        params={"title": title}
    )
    # print([manga["id"] for manga in r.json()["data"]])

    json = r.json()["data"]

    #return [get_manga(manga['id']) for manga in json]

    for manga in json:
        title = f"{manga['attributes']['title']['en']}"
        id = manga['id']

        print(f'{title} | ({id})')
        manga = get_manga(id)

        manga.show()

    return []