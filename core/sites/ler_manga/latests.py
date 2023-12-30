import math
from typing import Callable

from bs4 import BeautifulSoup
from requests import get
from .constants import LINKS_PER_PAGE


def get_latest_updates(
    limit: int = LINKS_PER_PAGE, on_link_received: Callable[[str], None] = None
) -> list[str]:
    """
    Returns a list of all links from `lermmanga.org` that were updateds.\n
    Arguments:
        `limit:` the total quantity of manga links will be extracted.
    Return:
        A list of recent mangas updated.
    """
    total_pages = math.ceil(limit / LINKS_PER_PAGE)
    counter = 0
    links = []

    for i in range(1, total_pages + 1):
        url = f"https://lermanga.org/capitulos/page/{i}/"
        if i == 1:
            url = "https://lermanga.org/capitulos/"
        soup = BeautifulSoup(get(url).content, "html.parser")
        links_tags = soup.css.select("a.dynamic-visited")

        for a in links_tags:
            if counter == limit:
                break

            link = a.get("href")
            links.append(link)
            counter += 1

            if on_link_received != None:
                on_link_received(link)
    return links