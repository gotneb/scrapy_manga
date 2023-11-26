# External packages
from typing import Callable
from bs4 import BeautifulSoup, Tag
# Ours code
from requests import get

from .constants import *

TOTAL_LENGTH = 37

def get_populars(on_link_received: Callable[[str], None] = None) -> list[str]:
    """Visits the `readm.org` and returns most populars mangas right now."""
    url = "https://br.ninemanga.com/"
    links = []

    soup = BeautifulSoup(get(url).content, "html.parser")
    tags = soup.css.select("div.rightbox ul li a.show_book_desc")

    counter = 0
    for a in tags:
        link = a.get('href')
        links.append(links)

        if on_link_received != None:
            on_link_received(link)
        
        counter += 1
        if counter >= TOTAL_LENGTH:
            break

    return links