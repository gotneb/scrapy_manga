from typing import Callable
from bs4 import BeautifulSoup
from requests import get


def get_populars(on_link_received: Callable[[str], None] = None) -> list[str]:
    """Visits the `lermanga.org` and returns most populars mangas right now."""
    URL = "https://lermanga.org/mangas/?orderby=trending&order=desc"
    soup = BeautifulSoup(get(URL).content, "html.parser")
    anchor_tags = soup.css.select("div.film-detail a")
    links = []
    for a in anchor_tags:
        link = a.get("href")
        links.append(link)

        if on_link_received != None:
            on_link_received(link)
    return links