from requests import get
from core.sites.mangadex_br.manga import get_manga

from entities.manga import Manga
from .constants import base_url

def search(title: str) -> list[Manga]:
    order = {
    "updatedAt": "desc",
}

    # Transform the order dictionary for deep object query parameters
    final_order_query = {
        f"order[{key}]": value for key, value in order.items()
    }

    r = get(
        f"{base_url}/manga",
        params=final_order_query
    )
    # print([manga["id"] for manga in r.json()["data"]])

    # print(r.content.decode())
    print(r.url)

    json = r.json()["data"]

    #return [get_manga(manga['id']) for manga in json]

    mangas = []
    for manga in json:
        title = f"{manga['attributes']['title']['en']}"
        id = manga['id']

        print(f'{title} | ({id})')
        manga = get_manga(id)
        mangas.append(manga)

        manga.show()

    return mangas