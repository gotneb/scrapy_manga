from typing import Callable
from bs4 import BeautifulSoup
from requests import get

from .constants import *

TOTAL_LENGTH = 37

def get_populars(on_link_received: Callable[[str], None] = None) -> list[str]:
    """Visits `br.ninemanga.com` and returns the most populars mangas right now."""
    url = "https://br.ninemanga.com/"
    links = []

    soup = BeautifulSoup(get(url).content, "html.parser")
    tags = soup.css.select("div.rightbox ul li a.show_book_desc")


    counter = 0
    for a in tags:
        link = a.get('href')
        links.append(link)

        if on_link_received != None:
            on_link_received(link)
        
        counter += 1
        if counter >= TOTAL_LENGTH:
            break

    return links